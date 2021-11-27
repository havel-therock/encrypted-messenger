# Structure of communication

Two mains object to communicate:
1. ClientRequest
2. ServerRequest

These classes contain fields:\
    request_type  < ENUM >\
    content < Any class > \
    content class should contain all necessary data for completion of request type 