# MacOS Chrome Password Decrypter

## TL;DR
Allows you to decrypt passwords saved in Google's Chrome Browser on Mac OS.

You will need access to:
* Mac OS Keychain and passwords with which entries are encrypted.
* Chrome's "Login Data" SQLite Database.

It is sufficient to obtain the required data from a backup, the device you are recovering the saved passwords from does not need to be operational.
This means you can easily pull the required data from a Timemachine backup for example.

## Introduction / HowTo
This is a very basic implementation and it offers no comforts. You will have to do most of the data gathering yourself. This is however intended. I created this script, as I was looking for a tool that would not heavily interact with my system, while trying to recover saved passwords from a Backup.
Google Chrome uses AES-128-CBC to encrypt / decrypt password kept in the SQLite database.

The AES key $DK$ is built as follows:

$DK = PBKDF2(PRF, Password, Salt, c, dkLen)$

where

- PRF = HMAC-SHA1
- Password = Provided Encryption Key
- Salt = "saltysalt"
- c = 1003 (Number of iterations)
- dkLen = 128 bit

### Gathering Files
From a backup or currently running system, you will need to recover the following files:

1) The SQLite Database containing the credentials: `~/Library/Application\ Support/Google/Chrome/Default/Login\ Data`
2) **Only when recovering from a Backup:** The Mac OS Keychain File: `~/Library/Keychains/login.keychain-db`

Copy these files into the directory where you have checked out this repository.

### Gathering Information

1) Using a SQLite Browser of your choice access the SQLite Database and determine the entry in the `logins` table you would like to decrypt. Copy the HEX value from the `password_value` column. This is the encrypted password.
2) Getting access to your Keychain
   1) In case you have copied the Keychain from a Backup, open the file using "Keychain", it will show as an additional "Login Keychain" in the sidebar. Work with this.
   2) In case you are working on a currently running system, open Keychain an open your "Login Keychain". Work with this.
3) Extracting Encryption Key from Keychain: In your keychain look for an entry called `Chrome Safe Storage`. Access the entry, copy the secret shown in Keychain. It will be a Base64 Encoded String.

### Decrypting the Password

Open the Decrypter script:

```
python3 macos-chrome-password-decrypter.py
Welcome to the Google Chrome Password Decrypter!
This is a dialog-based program. We are intentionally not using command line arguments, so that sensitive information does not end up in your shell history.
Please make sure to follow the provided instructions before proceeding.

Do you want to continue (y/n)? y
```

You will first be prompted for the Encryption Key:

```
Please provide the Google Chrome 'Safe Storage' encryption key (characters will not show).
Enter Encryption Key: 
```

After entering the key, you will be prompted for the encrypted password:

```
Please provide the encrypted password as a hex string. String must be 19 bytes long.
Enter with or without spaces. For example: 'de ad be ef ...' or 'deadbeef ...'
Enter Hex Dump: 76 31 30 5A 76 E0 48 85 E3 D6 A0  13 2D 42 C7 BE B7 4A B1
```
After pressing `ENTER, the decoded password will be shown:
```
Password: TextMustBe16Byte
```

### Test Data

I want to test this *right now*, but I do not have the files at hand.

Say no more:

- Use Encryption Key: `TEST`
- Use Encrypted Password: `76 31 30 5A 76 E0 48 85 E3 D6 A0 13 2D 42 C7 BE B7 4A B1`
- This will return: `TextMustBe16Byte`
