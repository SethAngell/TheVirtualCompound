# Blog

The Blogging backend will power first and foremost, the blogging portion of the site. It supports header images and opengraph protocol metadata. In the future, the intention is for the BlogPost class to parent other, more specific forms of textual data.

## Data Model

```mermaid
classDiagram
    class Blog {
        +string blog_name
        +string blog_description
        +fk[CustomUser] blog_owner
    }

    class TopicTags {
        +string tag_name
    }

    class PostImage {
        +string reference
        +string alt_text
        +image image
        +image thumbnail

        -make_thumbnail()
        -generate_png_version(p_image, p_name)
    }

    class BlogPost {
        +string title
        +string markdown_body
        +string html_body
        +string preview
        +string slug
        +datetime created_date
        +datetime updated
        +string visibility
        +fk[PostImage] header_image
        +fk[Blog] parent_blog
        +string image_encoding
        +string open_graph_protocol_description

        -pretty_preview()
        -determine_image_encoding()
        -extension()
        -extract_title()
        -classify_components()
    }

    TopicTags "0..*" --> "0..*" BlogPost : describe
    BlogPost "0..*" --> "1" Blog : Belongs to
    PostImage "1" --> "1" BlogPost : advertise
```
