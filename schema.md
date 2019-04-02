| Token |
| :------------- | :------------- | :------------- |
| Token (text)   | Token ID (int) | Primary Key (Token) |
- each token, uniquely ID'ed


| Posting |
| :------------- | :------------- | :--------- | :------- | :------- |
| Token ID  (int)     | Doc Id   (int)      |  Offset  (int)  | Before (int)  | After (int)   |
- a token's location in a given piece, its offset, the token before and after it

| Index |
| :------------- | :------------- |
| Token_idx      | Token       |
- an unique index created for each token
