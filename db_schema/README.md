### Task 3: PostgreSQL Database Schema

The cleaned and analyzed review data is stored in a PostgreSQL database named `bank_reviews`. The schema follows a simple star-like model with a **Dimension Table** (`banks`) and a **Fact Table** (`reviews`).

#### 1. Banks Table (Dimension)

Stores unique bank and application identifiers.

| Column Name     | Data Type      | Key             | Description                                                |
| :-------------- | :------------- | :-------------- | :--------------------------------------------------------- |
| **`bank_id`**   | `SERIAL`       | **PRIMARY KEY** | Unique auto-generated ID for each bank.                    |
| **`bank_name`** | `VARCHAR(255)` | UNIQUE          | Full name of the bank (e.g., Commercial Bank of Ethiopia). |
| **`app_name`**  | `VARCHAR(255)` |                 | Name of the mobile application.                            |

---

#### 2. Reviews Table (Fact)

Stores the scraped data and the results of the sentiment and thematic analysis.

| Column Name           | Data Type       | Key             | Description                                                             |
| :-------------------- | :-------------- | :-------------- | :---------------------------------------------------------------------- |
| **`review_id`**       | `VARCHAR(50)`   | **PRIMARY KEY** | Unique ID for the review (from scraping/source).                        |
| **`bank_id`**         | `INTEGER`       | **FOREIGN KEY** | Links review to the `banks.bank_id`.                                    |
| **`review_text`**     | `TEXT`          |                 | The raw text of the user review.                                        |
| **`rating`**          | `INTEGER`       |                 | The star rating (1 to 5).                                               |
| **`review_date`**     | `DATE`          |                 | Date the review was published. (If available in your data)              |
| **`sentiment_label`** | `VARCHAR(50)`   |                 | The categorical VADER sentiment label (Positive, Negative, Neutral).    |
| **`sentiment_score`** | `NUMERIC(5, 4)` |                 | The VADER compound score (-1.0000 to 1.0000).                           |
| **`theme`**           | `VARCHAR(255)`  |                 | The primary theme assigned (e.g., 'core-functionality', 'performance'). |
| **`source`**          | `VARCHAR(50)`   |                 | Source platform (Default: 'Google Play Store').                         |

---

### SQL Dump Command for Reproduction

The following command was used to generate the schema file (`db_schema/schema_and_banks_data.sql`), which can be used to recreate the structure:

```bash
# Gets schema of all tables (-s) and data for the banks table (-a --table banks)
pg_dump -U postgres -d bank_reviews -s > db_schema/schema_only.sql
pg_dump -U postgres -d bank_reviews -a --table banks >> db_schema/schema_only.sql
```
