# EventManager
Event Manager is a simple event manager application using Python.

## Steps To RUN
- Copy `.env.sample` to `.env`
- Run `docker-compose up`
- Run in another terminal
  ```shell
  $ docker exec -it event_api bash
  $ python manage.py createsuperuser
  # Enter admin details in the prompt
  ```
  - Open `http://localhost:3000/admin` in browser, it will open django admin


## API Details
- `/users/login` to login
- `/users/register` to sign up
- `/events` to create and list event
- `/events/<id>` to get event details, update event and delete event
- `/events/<id>/bookings` to create and list bookings
- `/events/bookings/<id>` to get booking details
- `/events/<id>/sumarry` to get summary of event