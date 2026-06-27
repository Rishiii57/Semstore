# **Assignment 1: The "Box Office Bomb" Data Pipeline**

**Total Marks: 20**

**Deadline: 7:00 PM, 22nd January, 2026**

## **Background Story**

You are working as a data engineer at a media analytics startup. Your team is conducting a study on financial failures in the film industry. They want to understand the relationship between **Production Budgets**, **Estimated Losses**, and **Critical Reception** (IMDb/Metacritic scores).

There is no clean dataset available. You have identified a Wikipedia page, **"[List of biggest box-office bombs](https://en.wikipedia.org/wiki/List_of_biggest_box-office_bombs),"** as your primary source. However, this data is meant for human eyes, not machines. It contains:

* **Visual noise:** Status symbols (e.g., §, †) attached to titles.  
  ![][image1]  
* **Ambiguous numbers:** Budgets and losses are often ranges (e.g., *"$100–160"*).  
  ![][image2]  
* **Messy references:** Footnotes (e.g., \[nb 2\]) and currency symbols mixed with values.  
  ![][image3]

Your manager has adopted a **"Strict Schema"** policy. You must build a pipeline that ingests this dirty data, validates it using **Pydantic** to ensure type safety, and then enriches it via the OMDb API.

## **Your Objective**

Design and implement an end-to-end pipeline that:

1. **Scrapes** the specific "Box Office Bomb" table from Wikipedia.  
2. **Validates & Cleans** the data using **Pydantic models** (converting ranges to averages, stripping symbols).  
3. **Enriches** the valid entries with metadata (Plot, Ratings) using the OMDb API.  
4. **Categorizes** the financial impact for analysts.

## 

## **Tasks & Evaluation**

### **Task 1: Scrape the "Bombs" Table (4 Marks)**

Story context:

The data is locked in an HTML table. You need to extract the raw text exactly as it appears before attempting to clean it.

**Task:**

1. Target the URL: https://en.wikipedia.org/wiki/List\_of\_biggest\_box-office\_bombs  
2. Programmatically extract the main table: **"Biggest box-office bombs"**.  
3. Parse the following **raw string columns** for every row:  
   * **Film Title** (e.g., *"Jungle Cruise §"*)  
   * **Year** (e.g., *"2021"*)  
   * **Net production budget** (e.g., *"$200"* or *"$100–160"*)  
   * **Estimated loss** (Target the **"Nominal"** column, not the inflation-adjusted one).

**Evaluation:**

* **Targeting:** Correctly identifies the table and handles the nested headers (Budget vs Loss sub-columns). (2 marks)  
* **Extraction:** Accurate extraction of raw strings for all rows without losing data. (2 marks)

**Note:**

When extracting the movie titles, you need to extract the entire raw string with the symbols, references, etc along with the titles. To extract the complete text content of an element, including any symbols or characters outside nested tags, use the **.get\_text()** method directly on the **parent element**. For example: text \= soup.th.get\_text()

---

### **Task 2: Pydantic Data Parsing & Validation (6 Marks)**

Story context:

"Garbage In, Garbage Out." Your manager forbids passing raw strings to the analysis layer. You must implement a validation layer using Pydantic. This layer will act as a firewall, rejecting bad data and cleaning messy formats.

Task:

Define a Pydantic model class (e.g., MovieData) that implements the following validators:

1. **Title Cleaning:**  
   * Remove footnote markers (e.g., \[nb 2\], \[1\]).  
   * Remove special status symbols: § (streaming) and † (currently playing).  
   * *Example:* Input "Jungle Cruise §"  → Output "Jungle Cruise"  
2. **Numeric Parsing (Budget & Loss):**  
   * Strip currency symbols ($) and reference tags.  
   * **Handle Ranges:** If a value is a range (e.g., "100–160"), you must parse both numbers and calculate the **average**.  
   * *Example:* Input "$100–160" → Output 130.0 (float).  
3. **Year Validation:**  
   * Ensure the year is a valid integer.

**Implementation Constraint:**

* You must use Pydantic's @field\_validator (v2) or @validator (v1) decorators.  
* Rows that fail validation (e.g., unparsable numbers) must be dropped or logged, but **must not crash the script**.

**Evaluation:**

* **Regex Logic:** Correct patterns to clean Titles (handling specific symbols §, †). (2 marks)  
* **Range Handling:** Logic to parse hyphens/en-dashes in budgets and calculate averages. (2 marks)  
* **Pydantic Usage:** Effective use of the model to enforce float and int types. (2 marks)

---

### **Task 3: Enrich with OMDb Data (4 Marks)**

Story context:

Financial data tells us how much money was lost, but it doesn't explain why. Was it a bad script? A specific director? We need metadata to find the root cause.

Task:

For each validated movie object from Task 2:

1. Query the OMDb API using the clean **Title** and **Year**.  
2. Extract and store the following specific fields from the JSON response:  
   * **Plot**  
   * **Metascore** (e.g., "40")  
   * **imdbRating** (e.g., "5.6")  
   * **Director** (e.g., "Oliver Stone")  
   * **Language** (e.g., "English")  
       
3. **Error Handling:**  
   * If the API returns Response: "False", or if a specific field is "N/A", ensure your code handles this gracefully (store as None or NaN).  
   * **Do not** discard the Wikipedia row just because OMDb is missing data.

**Evaluation:**

* Correct construction of the API request parameters. (1 mark)  
* Accurate extraction of the 5 required fields. (2 marks)  
* Robust handling of missing data (converting "N/A" strings to None). (1 mark)  
  ---

  ### **Task 4: Data Consistency Check (2 Marks)**

Story context:

APIs are not perfect. Sometimes querying "The Mummy" returns the 1999 hit instead of the 2017 flop.

**Task:**

1. Compare the **Wikipedia Year** with the **OMDb Year**.  
2. Create a column Match\_Status:  
   * **"Verified"**: Year's match (allow a tolerance of ±1 year for release differences).  
   * **"Mismatch"**: Years differ by \>1.  
   * **"Not Found"**: OMDb returned no data.

**Evaluation:**

* Correct logic for comparison (handling integers vs strings) and labeling. (2 marks)  
  ---

  ### **Task 5: Final Dataset & Categorization (4 Marks)**

Story context:

The final output will be consumed by financial analysts who group losses into tiers.

**Task:**

1. Create a Pandas DataFrame from your processed objects.  
2. Add a new column Loss\_Category based on your cleaned **Estimated Loss** column:  
   * **"Catastrophic"**: Loss ≥ $100M  
   * **"Severe"**: Loss between $50M and $100M  
       
   * **"Moderate"**: Loss \< $50M  
3. Save the result to box\_office\_failures.csv.

Required Columns:

Title, Year, Director, Language, Budget\_Millions, Loss\_Millions, Loss\_Category, IMDb\_Rating, Metascore, Match\_Status

**Evaluation:**

* Correct calculation of Loss\_Category using the cleaned float values. (2 marks)  
* Clean formatting of the final CSV (correct column headers, no dirty artifacts). (2 marks)  
  ---

  ## **Submission Requirements**

* **Submit** the link to the collab notebook with all the cells run and the output visible. The collab notebook should be submitted with access to “IIT Gandhinagar”. No changes will be entertained after the submission deadline.  
* **Code Quality:** The code must be modular. The Pydantic model should be a distinct class definition.

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,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>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnAAAAAbCAYAAAD8v7ITAAAN+ElEQVR4Xu2c6XsVRRaH/VNmcxZXBEFwwX3cZnxccBdF5REGRBFl3GZgUESHR0ZEBDdGcUcWQRnBBQQfFgeyQTYQkpAEkhBCcANxvtTkrcvp1K3ue9OY67234/nwkuqq6uru4lTXr8+puse8tmCZURRFURRFUZLDMfzT3vGVoih54PAP/1MU5SeGec3PU5SjIQk2pAJOUfKIPwAVRck9SZh8leImCTakAk5R8og/ABVFyT1JmHyV4iYJNqQCTlHyiD8AFUXJPUmYfJXiJgk2pAJOUfKIPwAVRck9SZh8leImCTakAq6ADB5TZt75pCmUL9wwpdI07O4M5Qt79h4wA+4sMc8v3WUGjioxLV3HtHf2PWVZz1MKhz8AFUXJPUmYfJXiJo4NnTWuzCxe0xYcnzO+3P69fXqt+e7QD2l1N1Z3ds3N5eatT1rtfP394VT+8Gk15uGX68zwx2vMM4uabB5tMrf71/NRAVdAzryrNJTn0pOAm7WowbzzabNN8/efb9bZ9B/vL896nlI4/AGoKEruiTP5Kko24tgQAk7SCLbRM7an8u9OCTmXYZMqA1E3c2GTWbau3bR3HrL5UmfI2O72VMAVOSLgEFsXdYmusU/Xmolzv7QqnnwE3JAxpebVFU1m4OhSU/nlvlAbwsQ52wMxpwKuePEHoJIcZj83x3Qe0P/Dnrj++htDefkmzuRbaIYOPTuUp0RTCJuKY0Mi4FaVdlhRNvX1Bus9+9ODW2yeXx8QbYO75vUD3xw2ayr2mxkLGoOyGx6tNnv2HbTpnAi46roO6+6jMeGaSVtD9aKord8fiBG4aWqV2Vi516bf/KjZjJxeEzonl/jXd7nxsSorlvx8FwTTBRMqQvm9YdrrO4M2XQF33r3d93nGkXwEXGltu03vaNxvrvpbdL+XVLdbg5BjFXDFiz8A43DBhReaFSs/SssbdNpg8+vfHGsGnDrI/v3u4KGg7PgTTrR5/fr3N7//w3Hm+8Pdrvxjf/s784tf/iqgEC/GpFHfsMv21QknnmT7r/+AgUHZvo79toy+ps8bm5qDsrOGDrV5pw0ebOtQ12+7L4Gd8rxiY5s2hyegKFuO20/LPlhuy6nP37kvvBCqI8SZfAvFjTcNt88LPAfP5dd5bs7c0Ngkj/pDTj/D/sUupWzEbXekjWvw20wi2Wzq4ksutWVnnpWyh3mvvJJ2roxbOebjy+8j4P/Dvy7EsSHXA4d4a+s4ZBpavjOzl3S/B1y++vawWbC6zTpkdjR/a71wCD8pv3lqtWlsy5GAQ8DQCALBzWeNFeuu/Po+M96pTxNptMU6LdK3Tqsyi1bvDp2TS/zru7D+bNXm1lC+y5wlDT2KvKMFZS5tugIOsSZ1JN8PoWYKueKl27uv+1gFXPHiD8CeuPyKK+1Lxp30nprxL3POuecFx+vXb7AvMdLjxt1trr3u+qBs4cJF5sqrrg6O+8qLPZ8g3CqrqgMPHH29eMnSoGzJe90veiYU/pZXbEkTetR3/8/6Gl98sSl4XoTHzrr6oC+EKFs+mn7iXPlQOXjo+6y2HGfyLQT0C2KENB44+QBw67z08jyb5wq4r77+Jq3elzt2WtuT4379B5jm3btD10sy2Wxqw4aNVvBLXeyC/nE/VkWg+e0KmzZtth+4fr4Qx4ZEwCG8XCcXkOfXF/CyXTSxItIDhwgk3WsBh1DDU+bnuyCQln2+JzieNG+HFU6IH3kQ8twHox5epu27OsywyVuth2/5+u426JT65k7rPbt71jabN2pGrT33zw9tMW3tKREojHsmVUYYsqklVeZe379nIL+5NVV3S5dQPbPrmtzHlFd2BnWunVwZiDwE0ogu0Rl1D9xn455OK0ppwxWmu7ryz59QYUUW3kzOlzbjCLjKHR02XdN1bpQHjnb9PBVwxYs/ALPBywdxwMvLnfSY4HwvhryoeJGXlHWvv5CvTtK84Cn3r6Nkh/7b33kgMoTqTxAct7XtNdU1tea4408I8vEOXHTxJaG2+wrY4zVHPhx8zxFksuUf209RwsclzuRbCBib8rEVFUKlf0aNGm37yO3H95f/xwpgty7P//U33wZpv62k05NN+dAHMj5Jd+zvzNoviMG6+oZQvhDHhlwP3NAj697YlODXg3PvrQjSDa0H7dq3n2wNHAIgk/hxwZOFeJFjwoOyVgsxQ+iPNKLGFSC0jfhAmBBWda9FGvHILkuEE+2Mf3abTT/xRp09lrqIncfm77Dphaub09pxr+9SUtMe1MMjSJpQJde78L4K89CLKQ/ZoNGlgcgjPfe9lNcRccixe78IUp4FMShtl29LXWdtaasVcoQ5XeEYR8BxnX8vb7Qu17qm9GfhPlHx9A2IcFQBV7z4AzAO/qTH8fz5rwfHItL4y6Tw2Zo1QVlj0+7gJcYkcOJJJ9sQK6FX8t0wjBLNmLFjzSkDTjVPz3wmUsDJJCrHIqAXLl5ij4Gwn+sd6GuIB+TdRYuzTra+LcPR9pPUbd8XvcYI4ky+hYBn496fnf1cpIATfAH390mTzfgJE9LqIHz5KOPjgjbdcGK28HJSiGtTQBja96a5H68+RDEIwfr5LnFsSARcTxsYYPHavWm7UBFv5NtdqC/tTNuFCr0ScKtL2npc/4Wg8kWeL4wkH08dwoc0As8VYXjbZN0XIsg9j8X5dz6VHgZFNFLPzYO65m7R6V/fBQ8hoUzS8gx+SDjq2YTy7d0ijftwnwWkDBG6dG23Z5FNBm6bmUKivUUFXPHiD8A4+JNeZXWNfTG1tLbaYzxyHPPCWv3ZZ/ZFTprJghCEvMSmTHnMPPTwI0E7hBD8MJcSzZrPP7cTBH1J6EZExh0jRwaigy9++hMBV1a+xabJox5h7UxrbfoKhDWH33JrILBWfpQu1MC35R/bT1u2VtprZFovF2fyLRTYyl13jQv6yV+7Bb6AQ7z5Au7kfqdYAbe1ssquiZV8ET6Z+iZJxLGpktKyyOfNJuDIJyTr57vEsSHXA5drfnIBRyjQ9apta+gINg2sLUvtxJAyHpRy0gg5wp5SRghW1qpR5q5b4zw8Zu51xbMmHi6B0Cb1o67vwj2zmUCOEWvDH0/FsGV9Gl5BOX9VSeo3WYTLu65z8cSK4H7dZ+G60ie+AKSue089/Q7cj0F/B6648QdgHPxJD6qqa60n7bTBQ0KhgnXr1luxMfTsc0JrZ3yylSnpSAj19jtGmltuHRHkPz7tCduP5DOp7mlpseEuPAfu+dRhQvLb7WtgrzJ5Yn9+mWvLveknwmszZ80K5UOcybfQ4IETsYXNuGW+gMP2Rv9lTFodztvbvi/ULmCH7lKKpJPJpt5+e0GkeINMAo71rG7YPhNxbMj/Hbhc0evfgSPMRwPu4nhANEn4kPVphPekbMQT1cGaNYQQni4pc8UMa8s+3NASHLvr6PwyvFTuz2ewoUI8XnTeuoq2oAxvHevQoq7vwvmyG9YXWRwjDhF4IvKo73r8bu4SeyL03HVycl3xNPpt8yyucFR+fvgDMA7+pOfDy99d0OzCy0rW3Awecrr5cMXKoCzTC05JRwSFCLjNJaUZw1/Sn70RJknk/r8+EAgMER4nndwvtLDet+W4/cSifcL+bh7nPv/ii2l5QpzJtxBwv7KWTWyI8emLLV/AsVZw4KBuL5uEYkk/+eT0UIgRrybLJ9y8pNGTTRFN8HfZu2R6v024737btp/vU6w25JJRwAGCjLVXm2varZCb/ladFSWyFos1WvO6BBwL+m87UhfPHWWE8d5flxJiVTs7rLdJ2kUAuuvmKBOPkV+GIJT1cCs3ttjry++d8dMb983ebtNPvpG6N/fHbOX6LhJaFWHKujTunWPxtJHGUyYij/tj7R35iET3HhB3sqYN8ECKp5G2uT/654pHttrzpE3l54k/AOPgT3rszpIXFxMdnjhCp5Sxi092bvGlyouckCvHiDeOyZfw6uR/TAldT0mHsB7rZRBwfOnT96+++potY4evTAaE9aQ/Jczd1tZujwkL9rTmJsnIpgKEFvb6xptvRYbnfVvuqZ8ok3WHtMcOTdIfLP/QlmWavIt18hWPG2MYAffpqlWRz+ELOMDu6FfS2CRrM0mLUMH+OB53z/i0kGpSyWZTCF7Sfr+5ZBJwfMiyi9XP9ylWG3LJKuAA0SQ7NCfMTnnXBHZ8Iq6A9WesY5OfCZm/oskKlv9WpsQfOzFZcO+vLXOP/TJh5rv19vrsMuU6ko8wol2EI+ISsceOV//6bluEON0NCFzT3V0qu1hdkSfPiSB7+YNd9jfk8DzyrJnWvwGiU3agyuYG36Op/LzwB2Ac/EkPJEzK74/VbtueVvbe0mX25UZ41feA8JJH8HHuyo8/Dl1LiYbf4KJP6Tf63i2b+MCDdqIYdu11afn0Pf8HnMf5fpt9DUL5551/QdAXUZNrlC1n6ydXwNEeYeps7QvFPPnyAXXpZZfZ50Cs+t5GiBJwPO9VVw+z5xG2d8voI5ZMUPboo1ND7SWVTDZF35DnI7YCmQQcef57MYpitiGhRwGnKEru8AegkhyifkZECeMLj0KQhMk3UxheCVMIm0qCDamAU5Q84g9ARVFyTxImX6W4SYINqYBTlDziD0BFUXJPEiZfpbhJgg2pgFOUPOIPQEVRck8SJl+luEmCDamAU5Q84g9ARVFyTxImX6W4SYINqYBTlDziD0BFUXJPEiZfpbhJgg2pgFOUPOIPQEVRck8SJl+luEmCDamAU5Q84g9ARVFyTxImX6W4SYINWQGnKIqiKIqiJIf/AxuZ7AMLh/K4AAAAAElFTkSuQmCC>