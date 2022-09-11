SCHEMA_FIELD = {
  name: String,
  label: String,
  type: 'TYPE',
  optional: Boolean,
}

EXAMPLE_FIELD = {
  name: 'project_name',
  label: 'Project Name',
  type: 'STRING',
  optional: true,
}

RECORD_FIELD_STRING = {
  project_name: 'YYY PROJECT'
}

SCHEMA_FIELDGROUP = {
  name: String,
  label: String,
  // __type: 'FIELDGROUP',
  fields: [FIELD, FIELDGROUP, FIELDARRAY],  // having fields means its a fieldgroup
  // optional depends on the fields
}

EXAMPLE_FIELDGROUP = {
  name: 'Attendee',
  label: 'Attendee Details',
  // type: 'FIELDGROUP',
  fields: [
    // FIELD
    { name: 'attendee_name', label: 'Name of attendee', type: String },
    { name: 'attendee_designation', label: 'Designation of attendee', type: String },
    { name: 'attendee_age', label: 'Age of attendee', type: Int16Array },
    // FIELDGROUP
    { name: 'attendee_photo', label: 'Photo of attendee', fields: [
      { name: 'image', label: 'image file', type: Image },
      { name: 'uploadedAt', label: 'timestamp of upload', type: Int16Array },
      { name: 'uploadedBy', label: 'uploader', type: String }
    ] },
  ]
}

RECORD_FIELDGROUP = {
  // __type: 'Attendee',
  attendee_name: 'Max',
  attendee_designation: 'Manager',
  attendee_age: 17,
  attendee_photo: {
    image: null,
    uploadedAt: 3443453,
    uploadedBy: 'Jay'
  },
}

SCHEMA_FIELDARRAY = {
  name: String,
  label: String,
  list: [FIELD, FIELDGROUP, FIELDARRAY],  // having list means its a fieldarray, list is always array
  extendable: Boolean, // whether can add to array
}

EXAMPLE_FIELDARRAY = {
  name: 'projects',  // note, plural
  label: 'list of project names',
  list: { name: 'project_name', label: 'Project Name', type: 'STRING' },
  extendable: true,  
}

RECORD_FIELDARRAY = {
  projects: [ 
    'project1', 
    'project2',
  ],
  extendable: true,
  attendees: [
    { attendee_name: 'Max', attendee_designation: 'Manager', attendee_age: 17, attendee_photo: { image: null, uploadedAt: 3443453, uploadedBy: 'Jay' }, },
    { attendee_name: 'Tan', attendee_designation: 'Manager', attendee_age: 17, attendee_photo: { image: null, uploadedAt: 3443453, uploadedBy: 'Jay' }, },
    { attendee_name: 'Che', attendee_designation: 'Manager', attendee_age: 17, attendee_photo: { image: null, uploadedAt: 3443453, uploadedBy: 'Jay' }, },
  ],
}

SCHEMA_FIELD_MCQ = {
  name: String,
  label: String,
  type: 'MCQ',
  options: [{ key: String, value: String }],  // having options means its an MCQ
}

EXAMPLE_FIELD_MCQ = {
  name: 'project',
  label: 'project',
  options: [
    { key: 'project1', value: 'A&A at MK 22 LOT 55' },
    { key: 'project2', value: 'A&A at MK 22 LOT 77' },
  ],
}

RECORD_FIELD_MCQ = {
  project: 'project1',
}

reply = {
  project: '234 Woodlands Drive',
  attendees: [  // attendee
    { attendee_name: '', attendee_designation: '', attendee_photo: '', uploadedAt: 0, uploadedBy: '' },
    { attendee_name: '', attendee_designation: '', attendee_photo: '', uploadedAt: 0, uploadedBy: '' },
    { attendee_name: '', attendee_designation: '', attendee_photo: '', uploadedAt: 0, uploadedBy: '' },
    { attendee_name: '', attendee_designation: '', attendee_photo: '', uploadedAt: 0, uploadedBy: '' },
  ],
  issues: [// issue
    { issue_image: '', caption: '', description: '', remarks: '' },
    { issue_image: '', caption: '', description: '', remarks: '' },
    { issue_image: '', caption: '', description: '', remarks: '' },
    { issue_image: '', caption: '', description: '', remarks: '' },
    { issue_image: '', caption: '', description: '', remarks: '' },
  ],
  tags: [
    'aa', 'bb'
  ],
  createdAt: 0
}