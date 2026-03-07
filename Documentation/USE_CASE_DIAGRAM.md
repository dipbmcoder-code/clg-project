# Use Case Diagram - AI News Generator Project

```mermaid
usecaseDiagram
    actor "Admin" as admin
    actor "Registered User" as user
    actor "News Engine (System)" as system

    package "Authentication" {
        usecase "Login" as UC1
        usecase "Register" as UC2
        usecase "Logout" as UC3
    }

    package "Content Management" {
        usecase "Manage Posts" as UC4
        usecase "Manage Prompts" as UC5
        usecase "Manage Websites" as UC6
        usecase "Edit Post" as UC4a
        usecase "Delete Post" as UC4b
        UC4 <|-- UC4a
        UC4 <|-- UC4b
    }

    package "Automated News Pipeline" {
        usecase "Scrape News Sources" as UC7
        usecase "Generate Content (AI)" as UC8
        usecase "Publish to WordPress" as UC9
        usecase "Social Media Sharing" as UC13
    }

    package "Administration" {
        usecase "Manage Users" as UC10
        usecase "View System Logs" as UC11
        usecase "View Analytics Dashboard" as UC12
    }

    %% Admin Relationships
    admin --> UC1
    admin --> UC3
    admin --> UC4
    admin --> UC5
    admin --> UC6
    admin --> UC10
    admin --> UC11
    admin --> UC12

    %% User Relationships
    user --> UC1
    user --> UC2
    user --> UC3

    %% System Relationships
    system --> UC7
    system --> UC8
    system --> UC9
    system --> UC13
    
    %% System interactions with data managed by Admin
    UC8 ..> UC5 : <<uses>>
    UC9 ..> UC6 : <<uses>>
```

## Actors Description

1.  **Admin**: Has full access to the system. Can manage content, users, configuration (prompts/websites), and view system health.
2.  **Registered User**: Can register an account and log in. (Role capabilities can be expanded).
3.  **News Engine (System)**: The backend automated service (`news-engine`) that runs scheduled tasks to find, create, and publish news without human intervention.

## Text-Based Visual Representation (ASCII)

Since image generation services are currently experiencing high traffic, here is a visual representation of the Use Case Diagram:

```text
       Admin                                    System Boundary                                 News Engine
      (Actor)                                  +---------------------------------+             (System Actor)
                                               |                                 |
         O                                     |  (Authentication)               |                   [=/=]
        /|\                                    |    (O) Login                    |                     |
        / \  --------------------------------->|    (O) Register                 |                     |
         |                                     |                                 |                     |
         |                                     |  (Content Management)           |                     |
         |------------------------------------>|    (O) Manage Posts             |                     |
         |------------------------------------>|    (O) Manage Prompts           |<--------------------|
         |------------------------------------>|    (O) Manage Websites          |                     |
         |                                     |                                 |                     |
         |                                     |  (Automated Pipeline)           |                     |
    Registered                                 |    (O) Scrape News Sources      |<--------------------+
       User                                    |    (O) Generate AI Content      |<--------------------+
         O                                     |    (O) Publish to WordPress     |<--------------------+
        /|\ ---------------------------------->|                                 |
        / \                                    |   (Administration)              |
                                               |    (O) View Logs & Analytics    |
         |------------------------------------>|    (O) Manage Users             |
                                               |                                 |
                                               +---------------------------------+
```
