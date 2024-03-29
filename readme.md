# The Compound: Our little corner of the internet

[![Automated Site Deployment](https://github.com/SethAngell/TheVirtualCompound/actions/workflows/build-and-publish.yml/badge.svg?branch=main)](https://github.com/SethAngell/TheVirtualCompound/actions/workflows/build-and-publish.yml)

The compound is the next logical progression of my personal
portfolio site. A more dynamic, user friendly version which
my friends can use as a blog and general portfolio.

Built using Django, styled with Tailwind, contained in docker, proxied by nginx, and chugging away happily on Linode.

## ToDo:

A running list of tasks, both short term and long term.

### Short Term:

- [x] Rebuild Landing Page with Tailwind
  - [x] Create Wrightsville Outline
  - [x] Make outline selectable
  - [x] Make SVGs dynamic
  - [x] Add Dark Mode Support for SethHome and SethHomeOldSchool
- [x] Migrate blog from sethangell.com to here
- [x] Tie in Linode S3 for object storage
- [x] Create a footer
- [ ] Create a login/signup flow
- [x] Compile Tailwindcss properly to move away from the dev cdn

### Long Term:

- [ ] Add a _links_ section to the Landing Page to link things dynamically
- [ ] Store blog posts as `*.md` files in S3 and provide a txt only path to them
- [ ] Add a _collaborators_ acknowledgments section to blogs
- [ ] A what-are-all-of-those-files.md documents which details the different files and things in my repo. Something I wish I could have seen when I started and was inundated with dot-files (files that start with a '.')
- [ ] RSS Support for blogs
- [ ] _Templatize_ `blog` in a similar fashion to `profile`
- [x] Configure Github Actions
