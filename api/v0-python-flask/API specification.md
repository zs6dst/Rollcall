# Rollcall API specification
## Types
### Member
The *Member* struct describes a member
- *id*: (string) a unique identifier for a member
- *altId*: (string) alternative ID; eg. SAID
- *name*: (string) the member's first name
- *surname*: (string) the member's surname
- *language*: (string[1]) A=Afrikaans, E=English

## Methods
### *identify*
*identify* attempts to recognise a member from a photo.

- Usage: HTTP POST [url]/api/identify

- Request body:
    - *photo*: (string) the Base64 encoded image

- Response:
    - Body:
        - *photoId*: (string) unique photo ID (eg. GUID)
        - *member*: (*Member*) the member identified from the photo:

    - HTTP status:
        - 200 OK: member successfully identified; *photoId* and *member* not zero
        - 204 NOCONTENT: failed to identify member; *photoId* not zero, *member* zero
        - 400 BADREQUEST: photo unusable or not provided in request; *photoId* zero, *member* zero 
### *register*
*register* records the attendance of a member.

- Usage: HTTP POST [url]/api/register

- Input:
    - *photoId*: (string) the id of the photo returned by the *identify* method
    - *member*: (*Member* struct) which contains either:
        - *id*: (string) the unique member identifier; or 
        - *altId*: (string) alternate member ID (eg. SAID)

- Output:
    - *message*: (string) a suitable response message 

- HTTP status:
    - 201 CREATED: member's attendance successfully recorded
    - 204 NOCONTENT: member unknown
    - 400 BADREQUEST: *photoId* not provided or unknown 
    - 500 INTERNALERROR: the system failed to record the attendance