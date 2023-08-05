from typing import Any, Tuple

import imageio
import numpy

from neodroid.utilities import unity_specifications as US
from neodroid.utilities.spaces.range import Range
from neodroid.messaging.fbs import FBSModels as F


def deserialise_states(flat_states):
  states = {}

  for i in range(flat_states.StatesLength()):
    state = US.EnvironmentSnapshot(flat_states.States(i))
    states[state.environment_name] = state

  out_states = {}
  for key in sorted(states.keys()):  # Sort states by key, ensures the same order every time
    out_states[key] = states[key]

  simulator_configuration = US.SimulatorConfiguration(flat_states.SimulatorConfiguration(),
                                                      flat_states.ApiVersion())

  return out_states, simulator_configuration


def deserialise_configurables(flat_environment_description):
  configurables = {}
  if flat_environment_description:
    for i in range(flat_environment_description.ConfigurablesLength()):
      f_conf = flat_environment_description.Configurables(i)
      obs_type = f_conf.ConfigurableValueType()
      obs_value = f_conf.ConfigurableValue()
      observation_value, observation_space, _ = deserialise_sensor(obs_type, obs_value)

      configurable = US.Configurable(f_conf.ConfigurableName().decode(),
                                     observation_value,
                                     observation_space
                                     )
      configurables[configurable.configurable_name] = configurable
  return configurables


def deserialise_sensors(flat_description):
  out_sensors = {}

  for i in range(flat_description.SensorsLength()):
    f_obs = flat_description.Sensors(i)
    obs_type = f_obs.SensorValueType()
    obs_value = f_obs.SensorValue()
    sensor_value, sensor_space, is_image = deserialise_sensor(obs_type, obs_value)

    name = f_obs.SensorName().decode()
    out_sensors[name] = US.Sensor(name,
                                  sensor_space,
                                  sensor_value, is_image)
  return out_sensors


def deserialise_sensor(obs_type, obs_value):
  value = None
  value_range = None
  is_image = False
  if obs_type is F.FObservation.FSingle:
    value, value_range = deserialise_single(obs_value)
  elif obs_type is F.FObservation.FDouble:
    value, value_range = deserialise_double(obs_value)
  elif obs_type is F.FObservation.FTriple:
    value, value_range = deserialise_triple(obs_value)
  elif obs_type is F.FObservation.FQuadruple:
    value, value_range = deserialise_quadruple(obs_value)
  elif obs_type is F.FObservation.FArray:
    value, value_range = deserialise_array(obs_value)
  elif obs_type is F.FObservation.FETObs:
    value, value_range = deserialise_euler_transform(obs_value)
  elif obs_type is F.FObservation.FRBObs:
    value, value_range = deserialise_body(obs_value)
  elif obs_type is F.FObservation.FQTObs:
    value, value_range = deserialise_quaternion_transform(obs_value)
  elif obs_type is F.FObservation.FByteArray:
    value, value_range = deserialise_byte_array(obs_value)
    is_image = True
  elif obs_type is F.FObservation.FString:
    value, value_range = deserialise_string(obs_value)

  return value, value_range, is_image


def deserialise_observables(state):
  return [state.Observables(i) for i in range(state.ObservablesLength())]


def deserialise_unobservables(state):
  return US.Unobservables(state.Unobservables())


def deserialise_actors(flat_environment_description):
  actors = {}
  if flat_environment_description:
    for i in range(flat_environment_description.ActorsLength()):
      flat_actor = flat_environment_description.Actors(i)
      actor = US.Actor(flat_actor)
      actors[actor.actor_name] = actor

  out_actors = {}  # All dictionaries in python3.6+ are insertion ordered, actors are sorted by key and
  # inserted so that the order of actor key-value pairs are always the same for all instances the same
  # environment. This is
  # useful when descriptions are used for inference what value (motion strength) in a numeric vector
  # corresponds to what actor.
  for key in sorted(actors.keys()):
    out_actors[key] = actors[key]

  return out_actors


def deserialise_description(flat_description):
  return US.EnvironmentDescription(flat_description)


def deserialise_poses(unobservables):
  pl = unobservables.PosesLength()
  poses = numpy.zeros((pl, 7))
  for i in range(pl):
    pose = unobservables.Poses(i)
    pos = pose.Position(F.FVector3())
    rot = pose.Rotation(F.FQuaternion())
    poses[i] = [pos.X(), pos.Y(), pos.Z(), rot.X(), rot.Y(), rot.Z(), rot.W()]
  return poses


def deserialise_bodies(unobservables):
  bl = unobservables.BodiesLength()
  bodies = numpy.zeros((bl, 6))
  for i in range(bl):
    body = unobservables.Bodies(i)
    vel = body.Velocity(F.FVector3())
    ang = body.AngularVelocity(F.FVector3())
    bodies[i] = [vel.X(), vel.Y(), vel.Z(), ang.X(), ang.Y(), ang.Z()]
  return bodies


def deserialise_euler_transform(f_obs) -> Tuple[Any, Any]:
  transform = F.FETObs()
  transform.Init(f_obs.Bytes, f_obs.Pos)
  t = transform.Transform()
  position = t.Position(F.FVector3())
  rotation = t.Rotation(F.FVector3())
  direction = t.Direction(F.FVector3())
  # ranges = [q.XRange(),q.YRange(), q.ZRange()]

  return [[position.X(), position.Y(), position.Z()],
          [direction.X(), direction.Y(), direction.Z()],
          [rotation.X(), rotation.Y(), rotation.Z()],
          ], [None for _ in range(9)]


def deserialise_body(f_obs):
  body = F.FRBObs()
  body.Init(f_obs.Bytes, f_obs.Pos)
  b = body.Body()
  velocity = b.Velocity(F.FVector3())
  angular_velocity = b.AngularVelocity(F.FVector3())

  # ranges = [q.XRange(),q.YRange(), q.ZRange()]

  return [
           [velocity.X(), velocity.Y(), velocity.Z()],
           [angular_velocity.X(), angular_velocity.Y(), angular_velocity.Z()],
           ], [None for _ in range(6)]


def deserialise_quadruple(f_obs) -> Tuple[Any, Any]:
  q = F.FQuadruple()
  q.Init(f_obs.Bytes, f_obs.Pos)
  quad = q.Quat()
  data = [quad.X(), quad.Y(), quad.Z(), quad.W()]
  # ranges = [q.XRange(),q.YRange(), q.ZRange(), q.WRange()]
  return data, [None for _ in range(4)]


def deserialise_triple(f_obs) -> Tuple[Any, Any]:
  pos = F.FTriple()
  pos.Init(f_obs.Bytes, f_obs.Pos)
  position = pos.Vec3()
  value = [position.X(), position.Y(), position.Z()]
  value_range = [pos.XRange(), pos.YRange(), pos.ZRange()]
  return value, value_range


def deserialise_double(f_obs) -> Tuple[Any, Any]:
  pos = F.FDouble()
  pos.Init(f_obs.Bytes, f_obs.Pos)
  position = pos.Vec2()
  value = [position.X(), position.Y()]
  value_range = [pos.XRange(), pos.YRange()]
  return value, value_range


def deserialise_single(f_obs) -> Tuple[Any, Any]:
  val = F.FSingle()
  val.Init(f_obs.Bytes, f_obs.Pos)
  value, value_range = val.Value(), val.Range()
  return value, value_range


def deserialise_string(f_obs) -> Tuple[Any, Any]:
  val = F.FString()
  val.Init(f_obs.Bytes, f_obs.Pos)
  value = val.Str()
  return value, 'skip_observable_dim'


def deserialise_rigidbody(f_obs) -> Tuple[Any, Any]:
  qt = F.FRBObs()
  qt.Init(f_obs.Bytes, f_obs.Pos)
  position = qt.Body().Position(F.FVector3())
  rotation = qt.Body().Rotation(F.FQuaternion())
  data = [position.X(),
          position.Y(),
          position.Z(),
          rotation.X(),
          rotation.Y(),
          rotation.Z(),
          rotation.W(),
          ]
  return data, [Range(min_value=qt.VelRange().MinValue(),
                      max_value=qt.VelRange().MaxValue(),
                      decimal_granularity=qt.VelRange().DecimalGranularity())
                for _ in range(3)] + [Range(min_value=qt.AngRange().MinValue(),
                                            max_value=qt.AngRange().MaxValue(),
                                            decimal_granularity=qt.AngRange(

                                              ).DecimalGranularity()) for _ in
                                      range(4)]


def deserialise_quaternion_transform(f_obs) -> Tuple[Any, Any]:
  qt = F.FQTObs()
  qt.Init(f_obs.Bytes, f_obs.Pos)
  position = qt.Transform().Position(F.FVector3())
  rotation = qt.Transform().Rotation(F.FQuaternion())
  data = [position.X(),
          position.Y(),
          position.Z(),
          rotation.X(),
          rotation.Y(),
          rotation.Z(),
          rotation.W(),
          ]
  return data, [None for _ in range(7)]


def deserialise_byte_array(f_obs) -> Tuple[Any, Any]:
  byte_array = F.FByteArray()
  byte_array.Init(f_obs.Bytes, f_obs.Pos)
  data = byte_array.BytesAsNumpy()
  t = byte_array.Type()
  if t == F.FByteDataType.UINT8:
    out = numpy.frombuffer(data, dtype=numpy.uint8)
    out = out.reshape(*byte_array.ShapeAsNumpy())
    out = numpy.flipud(out)
  elif t == F.FByteDataType.FLOAT16:
    out = numpy.frombuffer(data, dtype=numpy.float16)
    out = out.reshape(*byte_array.ShapeAsNumpy())
    out = numpy.flipud(out)
  elif t == F.FByteDataType.FLOAT32:
    out = numpy.frombuffer(data, dtype=numpy.float32)
    out = out.reshape(*byte_array.ShapeAsNumpy())
    out = numpy.flipud(out)
  elif t == F.FByteDataType.PNG:
    out = imageio.imread(data, format='PNG-PIL')
  elif t == F.FByteDataType.JPEG:
    out = imageio.imread(data, format='JPEG-PIL')
  else:
    out = data
  return out, 'skip_observable_dim'


def deserialise_array(f_obs) -> Tuple[Any, Any]:
  array = F.FArray()
  array.Init(f_obs.Bytes, f_obs.Pos)
  # data = numpy.array([array.Array(i) for i in range(array.ArrayLength())])
  data = array.ArrayAsNumpy()
  return data, [None for _ in range(array.ArrayLength())]


def deserialise_actuators(flat_actor):
  '''

  # All dictionaries in python3.6+ are insertion ordered, actuators are sorted by key and
  # inserted so that the order of actuator key-value pairs are always the same for all instances the same
  # environment. This is
  # useful when descriptions are used for inference what value (motion strength) in a numeric vector
  # corresponds to what actuator.

  :param flat_actor:
  :return:
  '''
  actuators = {}
  for i in range(flat_actor.ActuatorsLength()):
    flat_actuator = flat_actor.Actuators(i)
    input_actuator = US.Actuator(flat_actuator.ActuatorName().decode(),
                                 flat_actuator.ActuatorRange()
                                 )
    actuators[input_actuator.actuator_name] = input_actuator

  out_actuators = {}
  for key in sorted(actuators.keys()):
    out_actuators[key] = actuators[key]

  return actuators


def deserialise_space(flat_space):
  if isinstance(flat_space, list):
    ret = []
    for space in flat_space:
      if space is not None:
        ran = Range(decimal_granularity=space.DecimalGranularity(),
                    min_value=space.MinValue(),
                    max_value=space.MaxValue()
                    )
        ret.append(ran)
      elif space != 'skip_observable_dim':
        ran = Range(decimal_granularity=10)
        ret.append(ran)

    return ret

  if isinstance(flat_space, str):
    if flat_space != 'skip_observable_dim':
      space = Range(decimal_granularity=10)
    else:
      return None
  else:
    space = Range(decimal_granularity=flat_space.DecimalGranularity(),
                  min_value=flat_space.MinValue(),
                  max_value=flat_space.MaxValue()
                  )

  return space
