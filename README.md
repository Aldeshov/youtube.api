# YouTube API `beta v1.0`
This Django project presents simple (only with basic functionalities) API for YouTube platform

---

## This API has features like

* User Authentication (JWT Authentication)
  * Profile
* Channel (Full Support)
  * Playlists
  * Contents
    * Comments
    
* Copyrights (Half Support)

### Authentication

This project uses `JWT Tokens` for Authentication

`BASE_URL/auth/register` - to register (First Step)

`BASE_URL/auth/login` - to get token

> App `Authentication` provides basic functionalities for User control

- Login / Register
- Get / Update / Delete User Information
- Get User by ID `Admin requires!`


### Channels & Contents

User can create Channel for storing Contents

`BASE_URL/apps/channels` - to create Channel

`BASE_URL/apps/channels/me` - Control User's Channel

> App `Applications` provides basic functionalities for User's Channel control and `read-only` other Channels 

- Create / Update / Delete User's Channel Information
- Watch / Control Subscription to other Channels

Subscription can be done by the url
`BASE_URL/channels/CODE/subscribe?undo=0`
where parameter `undo` can undo subscription if it is set to `1`

> App `Content` provides basic YouTube Content control and view

- Create / Update / Delete Content (Status, Playlist, Comment)
- View / Like (Dislike) / Save Content (Playlist)

`BASE_URL/apps/contents` - to create Content

`BASE_URL/apps/contents/me` - Control User's Contents

##### Also, User can create Status for Channel, add comments to Content, save playlists etc.

Urls for like / save - contents / playlists

`BASE_URL/apps/contents/CODE/save?undo=0` - Save content to profile (`undo=1` to undo)

`BASE_URL/apps/contents/CODE/like?dislike=0&retract=0` -Like content (`dislike=1` to dislike & `retract=1` to retract)

`BASE_URL/apps/playlists/CODE/save?undo=0` - Save playlist to profile (`undo=1` to undo)

All saved contents / playlists can be found from url:

`BASE_URL/auth/users/me/profile` - Profile url


### Additional `ADMIN only`

> App `Additional` provides Admin control of copyrights

At this moment have been released only two types of copyrights

* Game Copyright
* Song Copyright



All other features can be found in django project files

## Django Project description

- additional (app)
- applications (app)
- authentication (app)
- content (app)
- tools
- media (local only)
- venv (local only)
- youtube (base)
- gitignore
- manage.py (start)
- README.md
- requirements.txt (packages)


> Installation

* `python -m venv venv`
* `venv\Scripts\activate`
* `python -m pip install --upgrade pip`
* `pip install -r requirements.txt`
