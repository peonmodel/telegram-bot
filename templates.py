template = {
    "template_name": "toolbox_meeting_template_001",
    "document_title": "Toolbox Meeting",
    "version": "1.0.0",
    "description": "",
    "createdBy": "",
    "createdAt": 0,
    "fields": [
        {"label": "Fill in Project", "name": "project", "type": "MCQ", "description": "", "options": [
            {"key": "project1", "value": "XX project at MK 1 Lot 1"},
            {"key": "project2", "value": "YY project at WoodlandsX"},
            {"key": "project3", "value": "ZZ project at SembawangY"},
        ]},
        {"label": "Attendees", "name": "attendees", "extendable": True, "list": {
            "label": "Attendee Details", "name": "attendee", "fields": [
                {"label": "Name", "name": "attendee_name", "type": "String", "description": ""},
                {"label": "Designation", "name": "attendee_designation", "type": "String", "description": ""},
                {"label": "Photo of attendee", "name": "attendee_photo", "type": "Image", "description": ""},
                {"label": "uploadedAt", "name": "uploadedAt", "type": "Int", "description": ""},
                {"label": "uploadedBy", "name": "uploadedBy", "type": "String", "description": ""},
            ]
        }},

        {"label": "Safety Issues Raised", "name": "issues", "extendable": True, "list": {
            "label": "Issue", "name": "issue", "fields": [
                {"label": "Issue Image", "name": "issue_image", "type": "Image", "description": ""},
                {"label": "uploadedAt", "name": "uploadedAt", "type": "Int", "description": ""},
                {"label": "uploadedBy", "name": "uploadedBy", "type": "String", "description": ""},
                {"label": "Caption", "name": "caption", "type": "String", "description": ""},
                {"label": "Issue Raised By", "name": "issueRaisedBy", "type": "String", "description": ""},
                {"label": "Remarks", "name": "remarks", "type": "String", "description": ""},
            ]
        }},
        {"label": 'Tags', "name": 'tags', "extendable": True, "list": {
                "label": 'Tag', 
                "name": 'tag', 
                "type": 'String'
            }
        },
    ],
}
