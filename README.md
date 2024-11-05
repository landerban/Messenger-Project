Messenger Project

This is a real-time messenger application that enables secure and efficient communication between users. The project is built with Django, Django Channels, and WebSocket for real-time messaging capabilities, along with encryption for secure message storage and transfer.

Features

1. User Registration and Authentication

	•	Custom User Model: The application uses a custom user model with email as the primary identifier.
	•	Secure Registration and Login: Users can securely register and log in using their email and password.
	•	User Profile Management: Users can update their profile details, including first and last names.

2. Real-Time Messaging

	•	WebSocket-Based Messaging: Messages are sent and received in real-time using WebSocket, allowing instant communication between users.
	•	One-to-One Chat Rooms: Each chat session is private between two users, with unique chat rooms for each pair of users.
	•	Message Delivery Status: Messages are marked as “read” once viewed by the recipient.

3. Encryption and Security

	•	Encrypted Messages: Message content is encrypted using Fernet encryption before being stored in the database, ensuring that only the intended recipients can read the messages.
	•	Secure User Data: Sensitive user data, such as first and last names, is encrypted for enhanced privacy.
	•	Permissions: Only superusers and staff have access to certain administrative functions, ensuring data protection and role-based access.

4. Notification System

	•	Message Notifications: Users receive notifications for new messages, helping them stay updated with ongoing conversations.
	•	Real-Time Updates: Notifications are delivered in real-time, providing immediate alerts for any new activity.

5. Admin Panel Customization

	•	Admin Controls for User Management: The admin panel is customized to manage user accounts securely. Superusers can view and edit only specific fields.
	•	Message Management: Administrators can view encrypted messages and monitor chat activity for security and compliance.

6. User-Friendly Interface

	•	Responsive Chat Interface: The application includes a user-friendly and responsive chat interface, optimized for various device sizes.
	•	Profile Update Forms: Users can easily update their information through intuitive forms.

Technologies Used

	•	Backend: Django, Django Channels, WebSocket
	•	Frontend: HTML, CSS (you can specify if you used Bootstrap or any other framework)
	•	Database: SQLite (or specify if you used another database)
	•	Encryption: Cryptography (Fernet)
