# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/framework/formats/image_format.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/framework/formats/image_format.proto',
  package='mediapipe',
  syntax='proto2',
  serialized_pb=_b('\n.mediapipe/framework/formats/image_format.proto\x12\tmediapipe\"\xb9\x01\n\x0bImageFormat\"\xa9\x01\n\x06\x46ormat\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x08\n\x04SRGB\x10\x01\x12\t\n\x05SRGBA\x10\x02\x12\t\n\x05GRAY8\x10\x03\x12\n\n\x06GRAY16\x10\x04\x12\r\n\tYCBCR420P\x10\x05\x12\x0f\n\x0bYCBCR420P10\x10\x06\x12\n\n\x06SRGB48\x10\x07\x12\x0b\n\x07SRGBA64\x10\x08\x12\x0b\n\x07VEC32F1\x10\t\x12\x0b\n\x07VEC32F2\x10\x0c\x12\x08\n\x04LAB8\x10\n\x12\t\n\x05SBGRA\x10\x0b')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_IMAGEFORMAT_FORMAT = _descriptor.EnumDescriptor(
  name='Format',
  full_name='mediapipe.ImageFormat.Format',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SRGB', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SRGBA', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GRAY8', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GRAY16', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='YCBCR420P', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='YCBCR420P10', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SRGB48', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SRGBA64', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VEC32F1', index=9, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VEC32F2', index=10, number=12,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LAB8', index=11, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SBGRA', index=12, number=11,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=78,
  serialized_end=247,
)
_sym_db.RegisterEnumDescriptor(_IMAGEFORMAT_FORMAT)


_IMAGEFORMAT = _descriptor.Descriptor(
  name='ImageFormat',
  full_name='mediapipe.ImageFormat',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _IMAGEFORMAT_FORMAT,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=62,
  serialized_end=247,
)

_IMAGEFORMAT_FORMAT.containing_type = _IMAGEFORMAT
DESCRIPTOR.message_types_by_name['ImageFormat'] = _IMAGEFORMAT

ImageFormat = _reflection.GeneratedProtocolMessageType('ImageFormat', (_message.Message,), dict(
  DESCRIPTOR = _IMAGEFORMAT,
  __module__ = 'mediapipe.framework.formats.image_format_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.ImageFormat)
  ))
_sym_db.RegisterMessage(ImageFormat)


# @@protoc_insertion_point(module_scope)
