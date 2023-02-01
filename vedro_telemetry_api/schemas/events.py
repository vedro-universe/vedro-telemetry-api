from d42 import schema
from district42_exp_types.uuid_str import schema_uuid_str

__all__ = ("AnyEventSchema", "EventListSchema", "StartedTelemetryEvent", "ArgParseTelemetryEvent",
           "ArgParsedTelemetryEvent", "StartupTelemetryEvent", "ExcRaisedTelemetryEvent",
           "EndedTelemetryEvent",)

TimestampSchema = schema.int.min(0)

BaseEvent = schema.dict({
    "event_id": schema.str.len(1, ...),
    "session_id": schema_uuid_str,
    "created_at": TimestampSchema,
})

PluginSchema = schema.dict({
    "name": schema.str.len(1, ...),
    "module": schema.str.len(1, ...),
    "enabled": schema.bool,
    "version": schema.str.len(1, ...),
})

StartedTelemetryEvent = BaseEvent + schema.dict({
    "event_id": schema.str("StartedTelemetryEvent"),
    "project_id": schema.str.len(1, ...),
    "plugins": schema.list(PluginSchema),
    "inited_at": TimestampSchema,
})

ArgParseTelemetryEvent = BaseEvent + schema.dict({
    "event_id": schema.str("ArgParseTelemetryEvent"),
    "cmd": schema.list(schema.str).len(1, ...),
})

ArgParsedTelemetryEvent = BaseEvent + schema.dict({
    "event_id": schema.str("ArgParsedTelemetryEvent"),
    "args": schema.dict({...: ...}),
})

StartupTelemetryEvent = BaseEvent + schema.dict({
    "event_id": schema.str("StartupTelemetryEvent"),
    "discovered": schema.int.min(0),
    "scheduled": schema.int.min(0),
})

ExceptionSchema = schema.dict({
    "type": schema.str.len(1, ...),
    "message": schema.str,
    "traceback": schema.list(schema.str),
})

ExcRaisedTelemetryEvent = BaseEvent + schema.dict({
    "event_id": schema.str("ExcRaisedTelemetryEvent"),
    "scenario_id": schema.str.len(1, ...),
    "exception": ExceptionSchema,
})

EndedTelemetryEvent = BaseEvent + schema.dict({
    "event_id": schema.str("EndedTelemetryEvent"),
    "total": schema.int.min(0),
    "passed": schema.int.min(0),
    "failed": schema.int.min(0),
    "skipped": schema.int.min(0),
    "interrupted": ExceptionSchema | schema.none,
})

AnyEventSchema = schema.any(
    StartedTelemetryEvent,
    ArgParseTelemetryEvent,
    ArgParsedTelemetryEvent,
    StartupTelemetryEvent,
    ExcRaisedTelemetryEvent,
    EndedTelemetryEvent,
)

EventListSchema = schema.list(AnyEventSchema)
