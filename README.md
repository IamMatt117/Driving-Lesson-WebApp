# RoadReady

RoadReady is a web application designed to facilitate the booking of driving lessons for students and the purchase of courses. It's built on the Django framework and features a clean, attractive interface thanks to the use of Bootstrap for frontend design.

## Features

- **User Authentication**: RoadReady includes registration, login, and logout functionality, ensuring a secure and personalized user experience.
- **Booking System**: Students can easily book lessons with instructors, providing a seamless and efficient process for scheduling driving lessons.
- **Course Purchases**: In addition to booking lessons, students can also purchase driving courses directly through the platform.
- **Robust Data Models**: The application's data models are structured with various relationships, including many-to-many and foreign keys, allowing for complex and flexible data representation.
- **Access Permissions**: Views are properly configured with correct access permissions, ensuring that users can only access appropriate data and functionality.
- **Data Validation**: The application includes thorough data validation, ensuring the integrity and correctness of the data.
- **Attractive Design**: The use of Bootstrap for frontend design results in a nice, attractive site that enhances the user experience.

## Getting Started

To get started with RoadReady, you'll need to have Django installed.
```bash
pip install django
```
 Once you've installed Django, you can clone the RoadReady repository and navigate to the project directory. 

Then you need to install crispy forms
```bash
pip install django-crispy-forms
pip install crispy-bootstrap4
```
Before running the server, you must go to the right directory:
`cd assignment_2`

From there, you can use the Django development server to run the application:

```bash
python manage.py runserver
```

Then, open your web browser and navigate to `http://localhost:8000` to see the application in action.

## Authors
Arvind Rawat and Matthew Mahon

## Contributing

We welcome contributions to RoadReady! If you'd like to contribute, please fork the repository and make your changes. Once you're ready, submit a pull request. We'll review your changes and merge them in if everything looks good.


## Contact

If you have any questions or feedback, please feel free to get in touch. We'd love to hear from you!
Happy driving with RoadReady! 🚗
