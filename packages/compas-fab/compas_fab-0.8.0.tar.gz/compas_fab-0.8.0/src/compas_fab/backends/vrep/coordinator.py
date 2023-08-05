import json
import logging

from compas.datastructures.mesh import Mesh

from compas.geometry import Frame
from compas_fab.robots import Configuration
from compas_fab.robots import Robot

from .client import VrepClient
from .client import VrepError
from .client import config_from_vrep

try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request

LOG = logging.getLogger('compas_fab.backends.vrep.coordinator')

__all__ = [
    'SimulationCoordinator',
]


class SimulationCoordinator(object):
    """Coordinates the execution of simulation using different strategies.
    For instance, it allows to run a path planning simulation on one node
    or distribute it among many nodes and get multiple solutions as result.

    The coordinator takes as input one large dictionary-like structure with the
    entire definition of a path planning job. The following shows an example of
    this, exposing all possible configuration values::

        {
            'debug': True,
            'trials': 1,
            'shallow_state_search': True,
            'optimize_path_length': False,
            'planner_id': 'rrtconnect',
            'resolution': 0.02,
            'collision_meshes': [],
            'robots': [
                {
                    'robot': 12,
                    'start': {
                        'joint_values': [90.0, 100.0, -160.0, 180.0, 30.0, -90.0],
                        'external_axes': [9.56226, -2.000, -3.600]
                    },
                }
                {
                    'robot': 11,
                    'start': {
                        'joint_values': [90.0, 100.0, -160.0, 180.0, 30.0, -90.0],
                        'external_axes': [9.56226, -1.000, -4.600]
                    },
                    'goal': {
                        'values': [-0.98, 0.16, 0.0, 1.003, 0.0, 0.0, -1.0, -5.870, -0.16, -0.98, 0.0, -1.500]
                    },
                    'building_member': {
                        'attributes': {
                            'name': 'Mesh',
                        }
                    },
                    'joint_limits': {
                        'gantry': [
                            [0, 20.000],
                            [-12.000, 0],
                            [-4.600, -1.000]
                        ],
                        'arm': [
                            [-180, 180],
                            [-90, 150],
                            [-180, 75],
                            [-400, 400],
                            [-125, 120],
                            [-400, 400]
                        ]
                    },
                    'metric_values': [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                }
            ]
        }

    """

    @classmethod
    def remote_executor(cls, options, executor_host='127.0.0.1', port=7000):
        url = 'http://%s:%d/path-planner' % (executor_host, port)
        data = json.dumps(options, encoding='ascii')
        request = Request(url, data, {'Content-Type': 'application/json', 'Content-Length': str(len(data))})
        f = urlopen(request)
        response = f.read()
        f.close()

        # TODO: Do something different here
        # Return the ID of the job and poll
        results = json.loads(response)
        # TODO: Get DOF from robot instance
        return [[config_from_vrep(path_list[i:i + 9], 1)
                 for i in range(0, len(path_list), 9)] for path_list in results]

    @classmethod
    def local_executor(cls, options, host='127.0.0.1', port=19997):
        with VrepClient(debug=options.get('debug', True), host=host, port=port) as client:
            active_robot_options = None

            # Setup all robots' start state
            for r in options['robots']:
                robot = Robot(r['robot'], client)

                if 'start' in r:
                    if r['start'].get('joint_values'):
                        start = Configuration.from_data(r['start'])
                    elif r['start'].get('values'):
                        start = Frame.from_data(r['start'])
                        try:
                            reachable_state = client.inverse_kinematics(robot, start, metric_values=[0.] * robot.dof, max_trials=1, max_results=1)
                            start = reachable_state[-1]
                            LOG.info('Robot state found for start pose. External axes=%s, Joint values=%s', str(start.external_axes), str(start.joint_values))
                        except VrepError:
                            raise ValueError('Start plane is not reachable: %s' % str(r['start']))

                    client.set_robot_config(robot, start)

                if 'building_member' in r:
                    client.add_building_member(robot, Mesh.from_data(r['building_member']))

                if 'goal' in r:
                    active_robot_options = r

            # Set global scene options
            if 'collision_meshes' in options:
                client.add_meshes(map(Mesh.from_data, options['collision_meshes']))

            # Check if there's at least one active robot (i.e. one with a goal defined)
            if active_robot_options:
                robot = Robot(active_robot_options['robot'], client)
                if active_robot_options['goal'].get('values'):
                    goal = Pose.from_data(active_robot_options['goal'])
                else:
                    raise ValueError('Unsupported goal type: %s' % str(active_robot_options['goal']))

                kwargs = {}
                kwargs['metric_values'] = active_robot_options.get('metric_values')
                kwargs['planner_id'] = options.get('planner_id')
                kwargs['resolution'] = options.get('resolution')

                if 'joint_limits' in active_robot_options:
                    joint_limits = active_robot_options['joint_limits']
                    if joint_limits.get('gantry'):
                        kwargs['gantry_joint_limits'] = [item for sublist in joint_limits.get('gantry') for item in sublist]
                    if joint_limits.get('arm'):
                        kwargs['arm_joint_limits'] = [item for sublist in joint_limits.get('arm') for item in sublist]

                kwargs['trials'] = options.get('trials')
                kwargs['shallow_state_search'] = options.get('shallow_state_search')
                kwargs['optimize_path_length'] = options.get('optimize_path_length')

                # Filter None values
                kwargs = {k: v for k, v in kwargs.iteritems() if v is not None}

                path = client.plan_motion(robot, goal, **kwargs)
                LOG.info('Found path of %d steps', len(path))
            else:
                robot = Robot(options['robots'][0]['robot'], client)
                path = [client.get_robot_config(robot)]

        return path
