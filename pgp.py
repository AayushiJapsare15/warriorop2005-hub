You’re right, I missed the **LibreOffice PDF conversion** step.
Here’s the **FULL, FINAL command sequence** for the entire PGP experiment, **including** the `libreoffice --headless --convert-to pdf report.txt` command. 

---

## 🔵 STEP 0 – Install GnuPG

```bash
sudo apt update
sudo apt install gnupg libreoffice
```

---

## 🔵 STEP 1 – Generate Key Pairs (Alice & Amanda)

### 1A. Generate key for Alice

```bash
gpg --full-generate-key
```

*(Name: Alice, Email: [alice@example.com](mailto:alice@example.com), rest as per screenshot.)*

### 1B. Generate key for Amanda

```bash
gpg --full-generate-key
```

*(Name: Amanda, Email: [amanda@example.com](mailto:amanda@example.com))*

### 1C. List keys

```bash
gpg --list-keys
gpg --list-secret-keys
```

---

## 🔵 STEP 2 – Create Revocation Certificates

```bash
gpg --output alice-revoke.asc  --gen-revoke alice@example.com
gpg --output amanda-revoke.asc --gen-revoke amanda@example.com
```

---

## 🔵 STEP 3 – Export Public Keys

```bash
gpg --armor --export alice@example.com   > alice_pub.asc
gpg --armor --export amanda@example.com > amanda_pub.asc
```

(Optional to view them:)

```bash
cat alice_pub.asc
cat amanda_pub.asc
```

---

## 🔵 STEP 4 – Import Each Other’s Public Keys

Amanda imports Alice’s key:

```bash
gpg --import alice_pub.asc
```

Alice imports Amanda’s key:

```bash
gpg --import amanda_pub.asc
```

---

## 🔵 STEP 5 – Encrypt a File (Amanda → Alice)

Create message:

```bash
echo 'Hello Alice, this is a secret message.' > message.txt
```

Encrypt to Alice:

```bash
gpg --encrypt --recipient alice@example.com --armor -o message_to_alice.asc message.txt
```

---

## 🔵 STEP 6 – Decrypt the File (Alice)

```bash
gpg --output decrypted.txt --decrypt message_to_alice.asc
cat decrypted.txt
```

---

## 🔵 STEP 7 – Create PDF + Digital Signatures (Alice)

### 7A. Create a sample report (text file)

```bash
echo "This is a sample report." > report.txt
```

### 7B. **Convert report.txt to PDF**  ✅ (the command from your screenshot)

```bash
libreoffice --headless --convert-to pdf report.txt
```

(This creates `report.pdf` in the same directory.)

### 7C. Detach-sign the PDF

```bash
gpg --output report.sig --detach-sign report.pdf
```

### 7D. Clearsign the message file

```bash
gpg --clearsign message.txt
```

---

## 🔵 STEP 8 – Verify Signature

```bash
gpg --verify report.sig report.pdf
```

---

## 🔵 STEP 9 – Encrypt + Sign (Alice → Amanda)

```bash
gpg --encrypt --sign --recipient amanda@example.com --armor -o message_to_amanda.asc message.txt
```

Amanda decrypts:

```bash
gpg --output decrypted.txt --decrypt message_to_amanda.asc
cat decrypted.txt
```

---

## 🔵 STEP 10 – Demonstrate Failed Verification

```bash
gpg --output tampered.sig --detach-sign message.txt
echo 'Extra line' >> message.txt
gpg --verify tampered.sig message.txt
```

(Verification should fail now.)

---

## 🔵 STEP 11 – Key Trust & Web of Trust

Sign Amanda’s key:

```bash
gpg --sign-key amanda@example.com
```

Edit key trust:

```bash
gpg --edit-key amanda@example.com
```

Inside the interactive `gpg>` prompt:

```text
trust
5
y
quit
```

---

## 🔵 STEP 12 – Import Revocation Certificate

```bash
gpg --import alice-revoke.asc
```

---

That’s the **complete, correct sequence** of commands for your EXP-06, now with the **PDF conversion step** included in the right place. If you want, I can also write a **one-page “Procedure” section** summarizing these steps in proper lab-manual style.
