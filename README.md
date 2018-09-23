### User
* Roll Number (pk)
* Full Name
* Department
* Year

* Privilege Level
* Position

### Resume
* ID (Unique across all users)
* uID (user ID)
* Timestamp
* Status

### Section
* ID
* Title

### Point
* ID
* rID (resume ID)
* sID (section ID)
* position_in_list
* Type (Line / Block / Multicolumn)
* Status (None / Freeze / Pending / Verified / Denied)
* Verifier
* Status Comment
* Timestamp (For submission)

### Request
* ID
* sID
* User Privilege
* User Requester
* Content
* Timestamp
* Status

### Conversation
* ID
* uID1
* uID2

### Message
* cID
* uID
* Timestamp

### Notification
* ID
* uID1 (Receiver)
* uID2 (Sender)
* Status (Read/Unread)
* Timestamp