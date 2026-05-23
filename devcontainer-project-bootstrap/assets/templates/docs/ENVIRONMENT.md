# Environment

This project uses `.env.example` as the committed environment contract.

Do not commit `.env` or real secrets.

## Application Variables

| Variable | Required | Description |
| --- | --- | --- |
| `APP_ENV` | yes | Application runtime environment. |
| `APP_HOST` | yes | Interface used by the application inside the container. |
| `APP_PORT` | yes | Application port. |

## Local Services

Service variables are generated only for selected services.
