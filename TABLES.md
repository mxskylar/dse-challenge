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