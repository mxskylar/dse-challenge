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

| Column                    | Type        | Description                                                                                                                                                                                                                                       |
|---------------------------|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id                        | integer     | Unique value that joins to `timeslots.event_id`, `event_contacts.event_id` & `event_tags.event_id`                                                                                                                                                |
| event_campaign_id         | integer     | Joins to `event_campaigns.id`                                                                                                                                                                                                                     |
| sponsor_id                | integer     | Joins to `organizations.id`                                                                                                                                                                                                                       |
| event_type                | string      | The type of the event. Also included as a column in `attendances`.                                                                                                                                                                                |
| title                     | string      | The public name of the event                                                                                                                                                                                                                      |
| description               | string      | Long-form HTML description of the event                                                                                                                                                                                                           |
| featured_image_url        | string      | Path to the image for the event                                                                                                                                                                                                                   |
| high_priority             | boolean     | Whether the event is marked high priority for the provided organization                                                                                                                                                                           |
| timezone                  | string      | A timezone database string for the event, e.g., America/New_York.                                                                                                                                                                                 |
| browser_url               | string      | Canonical URL of the event                                                                                                                                                                                                                        |
| created_date              | integer     | Unix timestamp                                                                                                                                                                                                                                    |
| modified_date             | integer     | Unix timestamp                                                                                                                                                                                                                                    |
| visibility                | string enum | The visibility of the event                                                                                                                                                                                                                       |
| address_visibility        | string enum | The visibility of the event's address (which may be different from the visibility of the event itself)                                                                                                                                            |
| created_by_volunteer_host | boolean     | Whether the event was created by a volunteer host using our distributed organizing tool or not                                                                                                                                                    |
| is_virtual                | boolean     | Whether the event is virtual or not                                                                                                                                                                                                               |
| virtual_action_url        | string      | The url the event redirects to if it's an unshifted virtual event. Otherwise, null.                                                                                                                                                               |
| accessibility_status      | string enum | The degree of compliance with the Americans with Disabilities Act.                                                                                                                                                                                |
| accessbility_notes        | string      | Additional details about accessibility status and accomodations at the venue                                                                                                                                                                      |
| approval_status           | string enum | For a distributed organizing event, denotes where it is in the approval process.                                                                                                                                                                  |
| instructions              | string      | Private instructions sent to attendees of this event after signing up. Only exposed for authenticated list organization events or get organization event requests, for events owned by the authenticated user's organization. null otherwise.     |
| venue                     | string      | The name of the location, e.g., “Campaign HQ” or “Starbucks”. If the location is private, it will be the string This event’s address is private. Sign up for more details                                                                         |
| address                   | string      | The lines of the address. Should always have exactly two values in our system, which may be empty strings. If the location is private, the first line will be the string This event’s address is private. Sign up for more details                |
| locality                  | string      | The city                                                                                                                                                                                                                                          |
| region                    | string      | The two-character state code                                                                                                                                                                                                                      |
| country                   | string      | An ISO-3166-1 alpha-2 country code. Note that U.S. territories and commonwealths have their own country codes; e.g., Puerto Rico is PR. For create and update requests, the field is optional and defaults to US. Currently, only US is accepted. |
| postal_code               | string      | The geocoded location, or null if geocoding failed.                                                                                                                                                                                               |
| location_latitude         | float       | Latitude coordinate of the event location                                                                                                                                                                                                         |
| location_longitude        | float       | Longitude coordinate of the event location                                                                                                                                                                                                        |
| congressional_district    | string      | The Congressional district, or null if geocoding failed or no street address was provided                                                                                                                                                         |
| state_leg_district        | string      | The State Lower House district, or null if geocoding failed or no street address was provided                                                                                                                                                     |
| state_senate_district     | string      | The State Upper House/Senate district, or null if geocoding failed or no street address was provided                                                                                                                                              |

### event_contacts

Map of Mobilize [events](https://github.com/mobilizeamerica/api?tab=readme-ov-file#event-object) to [contacts](https://github.com/mobilizeamerica/api?tab=readme-ov-file#contact)

| Column             | Type    | Description              |
|--------------------|---------|--------------------------|
| event_id           | integer | Joins to `events.id`     |
| event_contact_uuid | string  | Joins to `contacts.uuid` |

### contacts

[Contacts](https://github.com/mobilizeamerica/api?tab=readme-ov-file#contact) for Mobilize events

| Column        | Type    | Description                                                                      |
|---------------|---------|----------------------------------------------------------------------------------|
| uuid          | string  | Unique value that joins to `event_contacts.event_contact_uuid`                                     |
| name          | string  | The name of the contact for the event.                                           |
| phone_number  | string  | The phone number of the contact for the event.                                   |
| owner_user_id | integer | The user_id of the user who owns the event. This is NOT guaranteed to be unique. |
| email_address | string  | The email address of the contact for the event.                                  |

### event_campaigns

[Campaigns](https://github.com/mobilizeamerica/api?tab=readme-ov-file#eventcampaign) for Mobilize events

| Column                | Type    | Description                                                              |
|-----------------------|---------|--------------------------------------------------------------------------|
| id                    | integer | Unique value that joins to `events.event_campaign_id`                                       |
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
| id     | integer | Unique value that joins to `event_tags.tag_id` |
| name   | string  | Text name of the tag         |