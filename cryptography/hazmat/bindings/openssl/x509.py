# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

INCLUDES = """
#include <openssl/ssl.h>

/*
 * This is part of a work-around for the difficulty cffi has in dealing with
 * `STACK_OF(foo)` as the name of a type.  We invent a new, simpler name that
 * will be an alias for this type and use the alias throughout.  This works
 * together with another opaque typedef for the same name in the TYPES section.
 * Note that the result is an opaque type.
 */
typedef STACK_OF(X509) Cryptography_STACK_OF_X509;
typedef STACK_OF(X509_REVOKED) Cryptography_STACK_OF_X509_REVOKED;
"""

TYPES = """
typedef ... Cryptography_STACK_OF_X509;
typedef ... Cryptography_STACK_OF_X509_REVOKED;

typedef struct {
    ASN1_OBJECT *algorithm;
    ...;
} X509_ALGOR;

typedef ... X509_ATTRIBUTE;

typedef struct {
    X509_ALGOR *signature;
    ...;
} X509_CINF;

typedef struct {
    ASN1_OBJECT *object;
    ASN1_BOOLEAN critical;
    ASN1_OCTET_STRING *value;
} X509_EXTENSION;

typedef ... X509_EXTENSIONS;

typedef ... X509_REQ;

typedef struct {
    ASN1_INTEGER *serialNumber;
    ASN1_TIME *revocationDate;
    X509_EXTENSIONS *extensions;
    int sequence;
    ...;
} X509_REVOKED;

typedef struct {
    Cryptography_STACK_OF_X509_REVOKED *revoked;
    ...;
} X509_CRL_INFO;

typedef struct {
    X509_CRL_INFO *crl;
    ...;
} X509_CRL;

typedef struct {
    X509_CINF *cert_info;
    ...;
} X509;

typedef ... X509_STORE;
typedef ... NETSCAPE_SPKI;
"""

FUNCTIONS = """
X509 *X509_new(void);
void X509_free(X509 *);
X509 *X509_dup(X509 *);

int X509_print_ex(BIO *, X509 *, unsigned long, unsigned long);

int X509_set_version(X509 *, long);

EVP_PKEY *X509_get_pubkey(X509 *);
int X509_set_pubkey(X509 *, EVP_PKEY *);

unsigned char *X509_alias_get0(X509 *, int *);
int X509_sign(X509 *, EVP_PKEY *, const EVP_MD *);

int X509_digest(const X509 *, const EVP_MD *, unsigned char *, unsigned int *);

ASN1_TIME *X509_gmtime_adj(ASN1_TIME *, long);

unsigned long X509_subject_name_hash(X509 *);

X509_NAME *X509_get_subject_name(X509 *);
int X509_set_subject_name(X509 *, X509_NAME *);

X509_NAME *X509_get_issuer_name(X509 *);
int X509_set_issuer_name(X509 *, X509_NAME *);

int X509_get_ext_count(X509 *);
int X509_add_ext(X509 *, X509_EXTENSION *, int);
X509_EXTENSION *X509_EXTENSION_dup(X509_EXTENSION *);
X509_EXTENSION *X509_get_ext(X509 *, int);
int X509_EXTENSION_get_critical(X509_EXTENSION *);
ASN1_OBJECT *X509_EXTENSION_get_object(X509_EXTENSION *);
void X509_EXTENSION_free(X509_EXTENSION *);

int X509_REQ_set_version(X509_REQ *, long);
X509_REQ *X509_REQ_new(void);
void X509_REQ_free(X509_REQ *);
int X509_REQ_set_pubkey(X509_REQ *, EVP_PKEY *);
int X509_REQ_sign(X509_REQ *, EVP_PKEY *, const EVP_MD *);
int X509_REQ_verify(X509_REQ *, EVP_PKEY *);
EVP_PKEY *X509_REQ_get_pubkey(X509_REQ *);
int X509_REQ_add_extensions(X509_REQ *, X509_EXTENSIONS *);
X509_EXTENSIONS *X509_REQ_get_extensions(X509_REQ *);
int X509_REQ_print_ex(BIO *, X509_REQ *, unsigned long, unsigned long);

int X509V3_EXT_print(BIO *, X509_EXTENSION *, unsigned long, int);
ASN1_OCTET_STRING *X509_EXTENSION_get_data(X509_EXTENSION *);

X509_REVOKED *X509_REVOKED_new(void);
void X509_REVOKED_free(X509_REVOKED *);

int X509_REVOKED_set_serialNumber(X509_REVOKED *, ASN1_INTEGER *);

int X509_REVOKED_add1_ext_i2d(X509_REVOKED *, int, void *, int, unsigned long);

X509_CRL *d2i_X509_CRL_bio(BIO *, X509_CRL **);
X509_CRL *X509_CRL_new(void);
void X509_CRL_free(X509_CRL *);
int X509_CRL_add0_revoked(X509_CRL *, X509_REVOKED *);
int i2d_X509_CRL_bio(BIO *, X509_CRL *);
int X509_CRL_print(BIO *, X509_CRL *);
int X509_CRL_set_issuer_name(X509_CRL *, X509_NAME *);
int X509_CRL_sign(X509_CRL *, EVP_PKEY *, const EVP_MD *);

int NETSCAPE_SPKI_verify(NETSCAPE_SPKI *, EVP_PKEY *);
int NETSCAPE_SPKI_sign(NETSCAPE_SPKI *, EVP_PKEY *, const EVP_MD *);
char *NETSCAPE_SPKI_b64_encode(NETSCAPE_SPKI *);
EVP_PKEY *NETSCAPE_SPKI_get_pubkey(NETSCAPE_SPKI *);
int NETSCAPE_SPKI_set_pubkey(NETSCAPE_SPKI *, EVP_PKEY *);
NETSCAPE_SPKI *NETSCAPE_SPKI_new(void);
void NETSCAPE_SPKI_free(NETSCAPE_SPKI *);

/*  ASN1 serialization */
int i2d_X509_bio(BIO *, X509 *);
X509 *d2i_X509_bio(BIO *, X509 **);

int i2d_X509_REQ_bio(BIO *, X509_REQ *);
X509_REQ *d2i_X509_REQ_bio(BIO *, X509_REQ **);

int i2d_PrivateKey_bio(BIO *, EVP_PKEY *);
EVP_PKEY *d2i_PrivateKey_bio(BIO *, EVP_PKEY **);

ASN1_INTEGER *X509_get_serialNumber(X509 *);
int X509_set_serialNumber(X509 *, ASN1_INTEGER *);

/*  X509_STORE */
X509_STORE *X509_STORE_new(void);
void X509_STORE_free(X509_STORE *);
int X509_STORE_add_cert(X509_STORE *, X509 *);
int X509_verify_cert(X509_STORE_CTX *);

const char *X509_verify_cert_error_string(long);

const char *X509_get_default_cert_area(void);
const char *X509_get_default_cert_dir(void);
const char *X509_get_default_cert_file(void);
const char *X509_get_default_cert_dir_env(void);
const char *X509_get_default_cert_file_env(void);
const char *X509_get_default_private_dir(void);
"""

MACROS = """
long X509_get_version(X509 *);

ASN1_TIME *X509_get_notBefore(X509 *);
ASN1_TIME *X509_get_notAfter(X509 *);

long X509_REQ_get_version(X509_REQ *);
X509_NAME *X509_REQ_get_subject_name(X509_REQ *);

Cryptography_STACK_OF_X509 *sk_X509_new_null(void);
void sk_X509_free(Cryptography_STACK_OF_X509 *);
int sk_X509_num(Cryptography_STACK_OF_X509 *);
int sk_X509_push(Cryptography_STACK_OF_X509 *, X509 *);
X509 *sk_X509_value(Cryptography_STACK_OF_X509 *, int);

X509_EXTENSIONS *sk_X509_EXTENSION_new_null(void);
int sk_X509_EXTENSION_num(X509_EXTENSIONS *);
X509_EXTENSION *sk_X509_EXTENSION_value(X509_EXTENSIONS *, int);
int sk_X509_EXTENSION_push(X509_EXTENSIONS *, X509_EXTENSION *);
X509_EXTENSION *sk_X509_EXTENSION_delete(X509_EXTENSIONS *, int);
void sk_X509_EXTENSION_free(X509_EXTENSIONS *);

int sk_X509_REVOKED_num(Cryptography_STACK_OF_X509_REVOKED *);
X509_REVOKED *sk_X509_REVOKED_value(Cryptography_STACK_OF_X509_REVOKED *, int);

/* These aren't macros these arguments are all const X on openssl > 1.0.x */
int X509_CRL_set_lastUpdate(X509_CRL *, ASN1_TIME *);
int X509_CRL_set_nextUpdate(X509_CRL *, ASN1_TIME *);
"""

CUSTOMIZATIONS = """
"""

CONDITIONAL_NAMES = {}
