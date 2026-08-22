# Meridian Pivot — Inventory Update MVP

## Overview

Meridian Pivot is an inventory update processing workflow built with Pipedream. It receives inventory updates through a webhook, validates the incoming data, determines the inventory status, and returns a decision through an HTTP response.

## Workflow

```text
Webhook Trigger
      ↓
Inventory Validation
      ↓
Meridian Pivot Decision
      ↓
Custom HTTP Response
```

## Input

The webhook accepts JSON inventory updates containing:

```json
{
  "sku": "SKU-001",
  "quantity": 10
}
```

## Validation

The workflow validates:

* SKU is provided
* Quantity is provided
* Quantity is a number
* Quantity is not negative

Invalid requests are rejected with an explanation.

## Decision Logic

|    Quantity | Decision       | Action                     |
| ----------: | -------------- | -------------------------- |
|           0 | `out_of_stock` | Flag item as out of stock  |
|         1–5 | `low_stock`    | Flag item for restocking   |
| More than 5 | `in_stock`     | Inventory level is healthy |

## Example

For:

```json
{
  "sku": "SKU-001",
  "quantity": 10
}
```

The workflow returns:

```json
{
  "status": "success",
  "decision": "in_stock",
  "action": "Inventory level is healthy"
}
```

## Technology

* Python
* Pipedream
* HTTP/Webhooks
* GitHub

## Status

The Meridian Pivot MVP is deployed and tested successfully using the live webhook endpoint.
