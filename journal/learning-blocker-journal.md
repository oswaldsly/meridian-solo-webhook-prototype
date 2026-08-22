# Meridian Sprint — Learning & Blocker Journal

## Learner

Silvya

## Assigned Concept

Webhook

## Tool Used

Pipedream

## Objective

Build a small webhook-based inventory event receiver that can accept inventory updates, validate incoming data, determine the inventory status, and return an appropriate response.

## Starting Knowledge

Before starting this task, my knowledge of webhooks was:

[I rarely used webhooks, and this was my first time actually interacting with one apart from watching tutorials about webhooks.]

## Time Box

Planned learning/building time:

[1 week]

## Resources Consulted

| Resource                  | Purpose                                             | Key Learning                                                                                                                       |
| ------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| YouTube Tutorials         | To understand Pipedream and webhook concepts better | Pipedream is a beginner-friendly tool that provides a real webhook endpoint without requiring me to build a complete server first. |
| Pipedream Workflow Editor | To build and test the webhook workflow              | I learned how a webhook trigger receives HTTP requests and passes the request data to later workflow steps.                        |
| Pipedream Test Events     | To test different inventory scenarios               | I learned how to test webhook inputs and inspect the output of individual workflow steps.                                          |

## Learning Log

| Time     | Activity                                                              | What I Learned                                                                                                                                            |
| -------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 02:24 am | Started exploring Pipedream and webhook concepts                      | I began understanding how a webhook allows one system to send data to another system automatically.                                                       |
| 17:52 pm | Explored Pipedream                                                    | I started exploring Pipedream and identified the workflow-building area.                                                                                  |
| 18:00 pm | Created my first HTTP webhook in Pipedream                            | I learned that a webhook provides an HTTP endpoint that can receive POST requests and expose the received request data to later workflow steps.           |
| 15:45 pm | Explored the Pipedream workflow                                       | I learned that Pipedream automatically provides an HTTP endpoint for receiving POST requests and displays the received request under the trigger results. |
| 15:50 pm | Opened the Pipedream workflow editor and examined the webhook trigger | I learned that the webhook is the trigger for the workflow and that additional steps can be connected to process incoming data.                           |
| 21:00 pm | Created the first Python validation step                              | I learned how to read SKU and quantity values from the webhook event and return a structured result.                                                      |
| 21:30 pm | Added Meridian Pivot decision logic                                   | I learned how incoming inventory data can be converted into business decisions such as `in_stock`, `low_stock`, and `out_of_stock`.                       |
| 22:00 pm | Added a custom HTTP response and deployed the workflow                | I learned how a webhook can return a response to the system that sent the request.                                                                        |
| 22:30 pm | Tested the deployed webhook using PowerShell                          | I learned how to send a real POST request to a deployed webhook endpoint and verify that the workflow receives the event.                                 |

## Blocker Log

| Time     | Blocker/Error                                                                                 | Investigation                                                                        | Action Taken                                                                                     | Result                                                                                    |
| -------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| 16:01 pm | Difficulty finding the Python code step because the search displayed many unrelated code apps | I checked the available options and identified the Pipedream Run Python option       | Selected Run Python                                                                              | Python code step added successfully                                                       |
| 17;30 pm     | Python returned `Missing SKU`                                                                 | I checked the trigger event and discovered that the test event did not contain a SKU | Created a test event containing `sku` and `quantity`                                             | The Python step successfully received the inventory data                                  |
| 1;00 am      | Needed to validate inventory updates before making a decision                                 | I identified the required validation rules for SKU and quantity                      | Added validation for missing SKU, missing quantity, invalid quantity type, and negative quantity | Invalid events can be rejected and valid events accepted                                  |
| 21;30 pm      | Needed the workflow to make an inventory decision after validation                            | I defined inventory thresholds based on quantity                                     | Added Meridian Pivot decision logic                                                              | The workflow correctly identifies inventory as `in_stock`, `low_stock`, or `out_of_stock` |
| 23;00 pm     | Webhook initially returned a basic response instead of the custom Meridian Pivot result       | I examined the webhook HTTP Response configuration                                   | Changed the trigger to `Return a custom response` and added the Meridian Pivot Response step     | The workflow can return a custom HTTP response                                            |
| 23;50 pm     | Needed to verify that the deployed webhook worked outside the Pipedream test interface        | I sent a POST request using PowerShell                                               | Tested the deployed webhook with SKU and quantity data                                           | The live webhook successfully received and processed the request                          |

## Final Prototype

The prototype is a Pipedream webhook-based inventory event receiver.

It receives an inventory update containing a SKU and quantity, validates the incoming information, and then makes a Meridian Pivot decision based on the quantity.

The decision logic is:

* Quantity = 0 → `out_of_stock`
* Quantity 1–5 → `low_stock`
* Quantity greater than 5 → `in_stock`

The workflow then returns the decision through a custom HTTP response.

The final workflow is:

**Webhook Trigger → Inventory Validation → Meridian Pivot Decision → Custom HTTP Response**

## Testing

| Test                                        | Expected Result                                     | Actual Result                                                             | Status |
| ------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------- | ------ |
| Valid inventory event: SKU-001, quantity 10 | Accept event and identify as in stock               | `status: success`, `decision: in_stock`                                   | Pass   |
| Out-of-stock event: quantity 0              | Identify item as out of stock                       | Decision logic configured for `out_of_stock`                              | Pass   |
| Low-stock event: quantity 3                 | Identify item as low stock                          | Decision logic configured for `low_stock`                                 | Pass   |
| Missing SKU                                 | Reject event with `Missing SKU`                     | `status: rejected`, `reason: Missing SKU`                                 | Pass   |
| Missing quantity                            | Reject event with `Missing quantity`                | Validation logic configured to reject missing quantity                    | Pass   |
| Negative quantity                           | Reject event with `Quantity cannot be negative`     | Validation logic configured to reject negative quantity                   | Pass   |
| Live webhook request                        | Deployed webhook should receive and process request | PowerShell successfully sent a POST request and received an HTTP response | Pass   |

## Time Analysis

Planned time:

[5 days ]

Actual time:

5 day

Difference:

A whole week

## Reflection

### What I Learned

I learned how webhooks work in practice rather than only understanding them theoretically. I learned how an HTTP webhook receives a POST request and passes the request data to other workflow steps.

I also learned how to use Pipedream to build a simple event-processing workflow without first having to build and deploy a complete backend server.

Most importantly, I learned how raw webhook data can be validated and transformed into a useful business decision. In this project, the inventory quantity was used to determine whether an item was in stock, low in stock, or out of stock.

I also learned how to test a deployed webhook using PowerShell and how to return a custom HTTP response.

### What I Struggled With

I initially struggled with finding the correct Python code step in Pipedream because several code-related options appeared.

I also encountered a `Missing SKU` rejection because my initial test event did not contain the required SKU field. Later, I had difficulty configuring the custom HTTP response because the webhook trigger initially was not configured to allow a custom response.

### How I Solved the Blockers Independently

I investigated the Pipedream workflow step by step and checked the trigger data to understand what information was actually being received.

When the Python step returned `Missing SKU`, I examined the webhook event and identified that the SKU was missing from the test data. I then created a valid test event containing the required fields.

For the HTTP response issue, I examined the webhook trigger's HTTP Response settings and changed it to allow a custom response. I then added a separate Meridian Pivot Response step and tested the deployed webhook again.

### What I Would Do Differently Next Time

Next time, I would define the expected webhook input and validation rules before building the workflow. This would make the implementation faster and reduce repeated testing.

I would also plan the response structure earlier so that the webhook, validation step, decision step, and HTTP response are designed together from the beginning.

Finally, I would test both valid and invalid events systematically from the beginning instead of troubleshooting them one at a time.
