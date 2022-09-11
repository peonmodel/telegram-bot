# [
#     {"key": "project.title", "value": "title"}, 
#     {"key": "project.ref", "value": "ref"}, 
#     {"key": "attendees.0.name", "value": "jon"}, 
#     {"key": "attendees.0.designation", "value": "pm"}, 
#     {"key": "attendees.0.photo", "value": "p1"}, 
#     {"key": "attendees.1.name", "value": "kon"},   <<<---- no index
#     {"key": "attendees.1.designation", "value": "wr"}, 
#     {"key": "attendees.1.photo", "value": "p2"}, 
#     {"key": "issues.0.image", "value": "image"}, 
#     {"key": "issues.0.caption", "value": "cap"}, 
#     {"key": "issues.0.raisedBy", "value": "jon"}, 
#     {"key": "issues.0.raisedAt", "value": "333"}, 
#     {"key": "issues.1.image", "value": "iii"}, 
#     {"key": "issues.1.caption", "value": "ccc"}, 
#     {"key": "issues.1.raisedBy", "value": "kon"}, 
#     {"key": "issues.1.raisedAt", "value": "444"}, 
#     {"key": "tags.0", "value": "xxx"},
#     {"key": "tags.1", "value": "yyy"},
# ]

simpletemplate = {
    "template_name": "simple_template_001",
    "document_title": "Simple Sample Template",
    "version": "1.0.0",
    "description": "",
    "createdBy": "",
    "createdAt": 0,
    "fields": [
        { "label": "Fill in Project Name", "key": "project_name", "type": "field", "description": "" },
        { "label": "Fill in Project Title", "key": "project_title", "type": "field", "description": "" },
        { "label": "Fill in Inspector Name", "key": "inspector_name", "type": "field", "description": "" },
        { "label": "Fill in Inspector Designation", "key": "inspector_designation", "type": "field", "description": "" },
        { "label": "Remarks5", "key": "remarks5", "type": "field", "description": "" },
        { "label": "Remarks6", "key": "remarks6", "type": "field", "description": "" },
    ],
}

template = {
    "template_name": "toolbox_meeting_template_001",
    "document_title": "Toolbox Meeting",
    "version": "1.0.0",
    "description": "",
    "createdBy": "",
    "createdAt": 0,
    "fields": [
        # MCQ is rather complicated, skipping

        # {"label": "Fill in Project", "key": "project", "type": "MCQ", "description": "", "options": [
        #     { "value": [
        #         { "key": 'project.title', "value": "Proposed A&A XX project at MK 1 Lot 1" },
        #         { "key": 'project.ref', "value": "A1234-12345-2021" },
        #         { "key": 'project.loc', "value": "123 Kranji Road 4" },
        #     ]},
        #     { "value": [
        #         { "key": 'project.title', "value": "Proposed A&A YY project at WoodlandsX" },
        #         { "key": 'project.ref', "value": "B1234-12345-2021" },
        #         { "key": 'project.loc', "value": "123 Woodlands Road 4" },
        #     ]},
        #     { "value": [
        #         { "key": 'project.title', "value": "Proposed A&A ZZ project at SembawangY" },
        #         { "key": 'project.ref', "value": "C1234-12345-2021" },
        #         { "key": 'project.loc', "value": "123 Sembawang Road 4" },
        #     ]},
        # ]},
        { "label": "Project Details", "key": "project", "type": "group" },
        { "label": "Project Title", "key": "project.title", "type": "field", "description": "" },
        { "label": "Project Reference", "key": "project.ref", "type": "field", "description": "" },
        # { "label": "Project Location", "key": "project.loc", "type": "field", "description": "" },

        { "label": "Attendees", "key": "attendees", "type": "list", "extendable": True },
        { "label": "Attendee Details", "key": "attendees.[attendee]", "type": "group" },
        { "label": "Add Attendee Name", "key": "attendees.[attendee].name", "type": "field", "description": "", "isItem": True },
        { "label": "Their Designation", "key": "attendees.[attendee].designation", "type": "field", "description": "", "isItem": True },
        { "label": "Their Photo (send image)", "key": "attendees.[attendee].photo", "type": "image", "description": "", "isItem": True, "isLastItem": True },
        # { "label": "uploadedAt", "key": "attendees.[attendee].uploadedAt", "type": "field", "description": "", "isItem": True },
        # { "label": "uploadedBy", "key": "attendees.[attendee].uploadedBy", "type": "field", "description": "", "isItem": True },

        { "label": "Safety Issues Raised", "key": "issues", "type": "list", "extendable": True },
        { "label": "Issue", "key": "issues.[issue]", "type": "group" },
        { "label": "Please send an Image of the issue", "key": "issues.[issue].image", "type": "image", "description": "", "isItem": True },
        # { "label": "uploadedAt", "key": "issues.[issue].uploadedAt", "type": "field", "description": "", "isItem": True },
        # { "label": "uploadedBy", "key": "issues.[issue].uploadedBy", "type": "field", "description": "", "isItem": True },
        { "label": "Issue Caption", "key": "issues.[issue].caption", "type": "field", "description": "", "isItem": True },
        { "label": "Raised By", "key": "issues.[issue].raisedBy", "type": "field", "description": "", "isItem": True },
        { "label": "Raised At", "key": "issues.[issue].raisedAt", "type": "field", "description": "", "isItem": True, "isLastItem": True },
        # { "label": "Remarks", "key": "issues.[issue].remarks", "type": "field", "description": "", "isItem": True },

        { "label": 'Add Tags', "key": 'tags', "type": 'list', "extendable": True },
        { "label": 'Tag', "key": 'tags.[tag]', "type": 'field', "isItem": True, "isLastItem": True },
        { "label": 'Email Address to send to', "key": 'email', "type": 'field' },
    ],
}

stored_templates = {
    'simple_template': simpletemplate,
    'toolbox_template': template,
}