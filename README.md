# Cactus Test Definitions

This repository contains YAML test procedure definitions for use with the CSIP-AUS Client Test Harness.

This repository also provides Python dataclasses to make it easier for Python code to work with these definitions. In addition, there are also helper functions for creating valid instances of these dataclasses directly from the YAML test procedure definition files.

Test Procedures can be found in the [cactus_test_definitions/procedures/](cactus_test_definitions/procedures/) directory


## Development / Testing

This repository also contains a small number of tests that verify that test definitions can be sucessfully converted to their equivalent python dataclasses.

First install the development and testing dependencies with,

```sh
python -m pip install --editable .[dev,test]
```

Once installed, run the tests with,

```sh
pytest
```

## Test Procedure Schema

A `TestProcedure` is a [YAML](https://yaml.org) configuration that describes how a CSIP-Aus Client test case should be implemented by a server / compliance body. It's designed to be human readable but interpretable by a test harness for administering a test. At its most basic level, a `TestProcedure` is a series of a "events" that a client must trigger in sequence in order to demonstrate compliance.

Here is a minimalist definition of a test case

```
Description: Minimal Test Case Definition
Category: Explaining Schemas
Classes:
  - Descriptive Test Tag 1
  - Descriptive Test Tag 2
Preconditions: 
    # See definitions below for more info
    actions:
    checks:
Criteria:
    # See definitions below for more info
    checks:
Steps:
    # See definitions below for more info
    STEP_NAME:
```

For how to actually interpret and "run" these test cases against a CSIP-Aus Server implementation, please see [cactus-runner](https://github.com/bsgip/cactus-runner) for a reference implementation.

## Steps/Events Schema

The most basic building block of a `TestProcedure` is a `Step`. Each `Step` will always define an `Event` which dictates some form of trigger based on client behavior (eg sending a particular request). When an `Event` is triggered, each of it's `Action` elements will fire which will in turn enable/disable additional `Steps` with new events and so on until the `TestProcedure` is complete. `Event`'s can also define a set of `Check` objects (see doco below) that can restrict an `Event` from triggering if any `Check` is returning False/fail.

When a `TestProcedure` first starts, normally only a single `Step` will be active but more can be enabled/disabled in response to client behaviour.

Step Schema:
```
Steps:
  DESCRIPTIVE_TITLE_OF_STEP: # This is used to reference this step in other parts of this test procedure
    event: # 
      type:  # string identifier of the event type - see table below
      parameters: # Any parameters to modify the default behaviour of the event - see table below
      checks: # A list of Check definitions that will need to be true for this event to trigger - see section on Checks below 
    actions:
       # See action schema in the Action section below
```

These are the currently defined `Event` types that a `Step` can define
| **name** | **params** | **description** |
| -------- | ---------- | --------------- |
| `GET-request-received` | `endpoint: str` `serve_request_first: bool/None` |  Triggers when a client sends a GET request to the nominated endpoint. Will trigger BEFORE serving request to server unless `serve_request_first` is `True` in which case the event will be triggered AFTER the utility server has served the request (but before being proxied back to the device client) |
| `POST-request-received` | `endpoint: str` `serve_request_first: bool/None` |  Triggers when a client sends a POST request to the nominated endpoint. Will trigger BEFORE serving request to server unless `serve_request_first` is `True` in which case the event will be triggered AFTER the utility server has served the request (but before being proxied back to the device client) |
| `wait` | `duration_seconds: str` |  Triggers `duration_seconds` after being initially activated |


### Actions

These are the currently defined `Action` elements that can be included in a test. `Action`'s can trigger at the beginning of a test (as a precondition) or whenever a `Step`'s `Event` is triggered.

`Action`'s are defined with the following schema, always as a list under an element called `actions`
```
actions: 
  - type: # string identifier of the action type - see table below
    parameters: # Any parameters to supply to the executed Action - see table below
```

This is an example of two `Action` elements that will enable a different Step and create a DERControl:

```
actions: 
  - type: enable-steps
    parameters:
      steps: NAME_OF_STEP_TO_ENABLE
  - type: create-der-control
    parameters:
      start: $now
      duration_seconds: 300
      opModExpLimW: 2000
```


| **name** | **params** | **description** |
| -------- | ---------- | --------------- |
| `enable-steps` | `steps: list[str]` | The names of `Step`'s that will be activated |
| `remove-steps` | `steps: list[str]` | The names of `Step`'s that will be deactivated (if active) |
| `set-default-der-control` | `opModImpLimW: float/None` `opModExpLimW: float/None` `opModLoadLimW: float/None` `setGradW: float/None` | Updates the DefaultDERControl's parameters with the specified values. |
| `create-der-control` | `start: datetime` `duration_seconds: int` `pow_10_multipliers: int/None` `primacy: int/None` `randomizeStart_seconds: int/None` `opModEnergize: bool/None` `opModConnect: bool/None` `opModImpLimW: float/None` `opModExpLimW: float/None` `opModGenLimW: float/None` `opModLoadLimW: float/None`| Creates a DERControl with the specified start/duration and values |
| `cancel-active-der-controls` | None | Cancels all active DERControls |
| `set-poll-rate` | `rate_seconds: int` | Updates the server poll rate for ALL list endpoints |
| `set-post-rate` | `rate_seconds: int` | Updates the server post rate for ALL endpoints listing a postRate |
| `communications-loss` | None | Simulates a full outage for the server (from the perspective of the client) |
| `communications-restore` | None | Reverses any active `communications-loss` state |
| `register-end-device` | `nmi: str/none` `registration_pin: int/None` | Creates a new `EndDevice`, optionally with the specified ConnectionPoint ID or PIN |


### Checks

A `Check` is a boolean test of the state of the utility server. They are typically defined as a success/failure condition to be run at the end of a `TestProcedure`.

`Check`'s are defined with the following schema, always as a list under an element called `checks`
```
checks: 
  - type: # string identifier of the check type - see table below
    parameters: # Any parameters to supply to the executed Check - see table below
```


This is an example of two `Check` elements that will check that all steps are marked as complete and that there has been a DERStatus submitted with specific values:

```
checks: 
  - type: all-steps-complete
    parameters: {}
  - type: der-status-contents
    parameters:
      genConnectStatus: 1
```

| **name** | **params** | **description** |
| -------- | ---------- | --------------- |
| `all-steps-complete` | `ignored_steps: list[str]/None` | True if every `Step` in a `TestProcedure` has been deactivated (excepting any ignored steps) |
| `connectionpoint-contents` | None | True if a `ConnectionPoint.id` has been set for the `EndDevice` under test |
| `der-settings-contents` | None | True if a `DERSettings` has been set for the `EndDevice` under test |
| `der-capability-contents` | None | True if a `DERCapability` has been set for the `EndDevice` under test |
| `der-status-contents` | `genConnectStatus: int/None` `operationalModeStatus: int/None` | True if a `DERStatus` has been set for the `EndDevice` under test (and if certain elements have been set to certain values) |
| `readings-site-active-power` | `minimum_count: int` | True if MUP for site wide active power has `minimum_count` entries |
| `readings-site-reactive-power` | `minimum_count: int` | True if MUP for site wide reactive power has `minimum_count` entries |
| `readings-site-voltage` | `minimum_count: int` | True if MUP for site wide voltage has `minimum_count` entries |
| `readings-der-active-power` | `minimum_count: int` | True if MUP for DER active power has `minimum_count` entries |
| `readings-der-reactive-power` | `minimum_count: int` | True if MUP for DER reactive power has `minimum_count` entries |
| `readings-der-voltage` | `minimum_count: int` | True if MUP for DER voltage has `minimum_count` entries |


### Parameter Variable Resolution

Any `parameter` element expects a series of name/value pairs to pass to the "parent" `Action`, `Check` or `Event`. For example:

```
parameters:
    number_param: 123
    text_param: Text Content
    date_param: 2020-01-02 03:04:05Z

```

But placeholder variables may also be used to reference things that aren't known until the test is underway. For example, the following would instead set `number_param` to the current DERSetting.setMaxW supplied by the client while `date_param` would be set to the moment in time that the `Action`, `Check` or `Event` is being evaluated.

```
parameters:
    number_param: $setMaxW
    text_param: Text Content
    date_param: $now

```

The following are all the `NamedVariable` types currently implemented

| **name** | **description** |
| -------- | --------------- |
| `$now` | Resolves to the current moment in time (timezone aware). Returns a datetime |
| `$setMaxW` | Resolves to the last supplied value to `DERSetting.setMaxW` as an integer. Can raise exceptions if this value hasn't been set (which will trigger a test evaluation to fail) |

Placeholder variables can also be used in some rudimentary expressions to make variations on the returned value. For example:

```
parameters:
    number_param: $(setMaxW / 2)
    text_param: Text Content
    date_param: $(now - '5 mins')
```

Would resolve similar to above, but instead `number_param` will be half of the last supplied value to `DERSetting.setMaxW` and `date_param` will be set to 5 minutes prior to now.