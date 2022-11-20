# Landing Page

The landing page is the heart of a user's profile. If implemented properly, the goal of the landing page + domain combo is to present as if this is the user's personal website. Obviously it is, but more specifically it should feel as if this site isn't living within a shared hosting space.

## Data Model

```mermaid
classDiagram
    class LandingPage {
        +fk[CustomUser] user
        +string name
        +string bio
        +string headline
        +image avatar
        +email contact_email
        +string instagram
        +string twitter
        +string github
        +string spotify
        +string linkedin
        +file resume
        +fk[Map] map_overlay
        +fk[Design] template
    }

    class FavoriteThing {
        +string thing_name
        +file svg_icon
        +string path_attribute
        +string viewbox_attribute
    }

    class Map {
        +string location_name
        +string overlay_name
    }

    class Design {
        +string template_name
        +string name
    }

    class Experience {
        +fk[CustomUser] user
        +string company
        +string title
        +string description
        +boolean present
        +integer start_year
        +integer end_year
        +url link
        +string link_title
    }

    FavoriteThing "0..*" --> "1" LandingPage : related
    LandingPage --> "1" Map : displays
    LandingPage --> "1" Design : presents
    Experience "0..*" --> "1" LandingPage : related
```
