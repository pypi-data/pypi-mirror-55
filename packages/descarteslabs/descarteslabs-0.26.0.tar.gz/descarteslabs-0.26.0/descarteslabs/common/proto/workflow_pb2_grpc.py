# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import workflow_pb2 as workflow__pb2


class WorkflowAPIStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.CreateWorkflow = channel.unary_unary(
        '/descarteslabs.workflows.WorkflowAPI/CreateWorkflow',
        request_serializer=workflow__pb2.CreateWorkflowRequest.SerializeToString,
        response_deserializer=workflow__pb2.Workflow.FromString,
        )
    self.ListWorkflows = channel.unary_stream(
        '/descarteslabs.workflows.WorkflowAPI/ListWorkflows',
        request_serializer=workflow__pb2.ListWorkflowsRequest.SerializeToString,
        response_deserializer=workflow__pb2.Workflow.FromString,
        )
    self.GetWorkflow = channel.unary_unary(
        '/descarteslabs.workflows.WorkflowAPI/GetWorkflow',
        request_serializer=workflow__pb2.GetWorkflowRequest.SerializeToString,
        response_deserializer=workflow__pb2.Workflow.FromString,
        )
    self.UpdateWorkflow = channel.unary_unary(
        '/descarteslabs.workflows.WorkflowAPI/UpdateWorkflow',
        request_serializer=workflow__pb2.UpdateWorkflowRequest.SerializeToString,
        response_deserializer=workflow__pb2.Workflow.FromString,
        )


class WorkflowAPIServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def CreateWorkflow(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ListWorkflows(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetWorkflow(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UpdateWorkflow(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_WorkflowAPIServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'CreateWorkflow': grpc.unary_unary_rpc_method_handler(
          servicer.CreateWorkflow,
          request_deserializer=workflow__pb2.CreateWorkflowRequest.FromString,
          response_serializer=workflow__pb2.Workflow.SerializeToString,
      ),
      'ListWorkflows': grpc.unary_stream_rpc_method_handler(
          servicer.ListWorkflows,
          request_deserializer=workflow__pb2.ListWorkflowsRequest.FromString,
          response_serializer=workflow__pb2.Workflow.SerializeToString,
      ),
      'GetWorkflow': grpc.unary_unary_rpc_method_handler(
          servicer.GetWorkflow,
          request_deserializer=workflow__pb2.GetWorkflowRequest.FromString,
          response_serializer=workflow__pb2.Workflow.SerializeToString,
      ),
      'UpdateWorkflow': grpc.unary_unary_rpc_method_handler(
          servicer.UpdateWorkflow,
          request_deserializer=workflow__pb2.UpdateWorkflowRequest.FromString,
          response_serializer=workflow__pb2.Workflow.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'descarteslabs.workflows.WorkflowAPI', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
