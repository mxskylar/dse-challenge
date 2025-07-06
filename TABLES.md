# Mobilize Event Tables

The following tables contain data about events managed with the Mobilize platform,
people who have attended the events, event contacts & sponsors, and more.

These tables can be used to answer questions, such as:

**How many people RSVP’d to an event with a given ID?**

```sql
SELECT COUNT(*)
FROM attendances
WHERE status IN ("REGISTERED", "CONFIRMED")
AND event_id = 91154;
```

**What event had the most number of completed attendances?**

```sql
SELECT MAX(num_completed), event_id
FROM (
    SELECT COUNT(*), event_id
    FROM attendances
    WHERE status = "CONFIRMED"
    GROUP BY 2
)
JOIN events
ON event_id = events.id;
```

## Tables

### attendances

### people

### custom_signup_field_values

### timeslots

### organizations

### events

[Events](https://github.com/mobilizeamerica/api?tab=readme-ov-file#event-object) managed in the Mobilize platform.

### event_contacts

Map of Mobilize [events](https://github.com/mobilizeamerica/api?tab=readme-ov-file#event-object) to [contacts](https://github.com/mobilizeamerica/api?tab=readme-ov-file#contact)

| Column        | Type    | Description                                                                      |
|---------------|---------|----------------------------------------------------------------------------------|
| uuid          | string  | Joins to `event_contacts.event_contact_uuid`                                     |
| name          | string  | The name of the contact for the event.                                           |
| phone_number  | string  | The phone number of the contact for the event.                                   |
| owner_user_id | integer | The user_id of the user who owns the event. This is NOT guaranteed to be unique. |
| email_address | string  | The email address of the contact for the event.                                  |

### contacts

[Contacts](https://github.com/mobilizeamerica/api?tab=readme-ov-file#contact) for Mobilize events

| Column             | Type    | Description              |
|--------------------|---------|--------------------------|
| event_id           | integer | Joins to `events.id`     |
| event_contact_uuid | string  | Joins to `contacts.uuid` |

### event_campaigns

[Campaigns](https://github.com/mobilizeamerica/api?tab=readme-ov-file#eventcampaign) for Mobilize events

| Column                | Type    | Description                                                              |
|-----------------------|---------|--------------------------------------------------------------------------|
| id                    | integer | Joins to `events.event_campaign_id`                                       |
| slug                  | string  | The public-facing slug of the event campaign.                            |
| event_create_page_url | string  | The URL of the public-facing event creation page for the event campaign. |

### event_tags

Map of Mobilize [events](https://github.com/mobilizeamerica/api?tab=readme-ov-file#event-object) to [tags](https://github.com/mobilizeamerica/api?tab=readme-ov-file#tag)

| Column   | Type    | Description          |
|----------|---------|----------------------|
| event_id | integer | Joins to `events.id` |
| tag_id   | integer | Joins to `tags.id`   |

### tags

[Tags](https://github.com/mobilizeamerica/api?tab=readme-ov-file#tag) for Mobilize events

| Column | Type    | Description                  |
|--------|---------|------------------------------|
| id     | integer | Joins to `event_tags.tag_id` |
| name   | string  | Text name of the tag         |