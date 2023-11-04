# PIR using PHE Homomorphic Encryption

This project is meant to auxiliar the study of
homomorphic algorithms. It is a web application
that allows the user to insert results into a 
database, and then, the user can query it.
However, it is not possible to know what query
the user has performed, due to the PIR protocol.

PIR stands for Private Information Retrieval. This
is a protocol that allows the user to query a database
using cryptographic primitives, without revealing
anything about the query. This project shows the steps
performed by the server and the client, being
transparent to the user.

## About Homomorphic Encryption

With Homomorphic Encryption (HE), you do not need
to decrypt the function with a private key to
evaluate some operation on it. In other words, for
applications like cloud computing, you can send your
encrypted data and the server will perform all the
operations you need, without knowing what is the data.

There are basically three variants of HE:
- Partially Homomorphic Encryption (PHE)
    - Makes one operation over ciphertext
- Somewhat Homomorphic Encryption (SHE)
    - Makes two operations over ciphertext (being one
      unlimited, normally addition and another limited,
      normally multiplication)
- Leveled Fully Homomorphic Encryption (LFHE)
    - It can evaluate additions and multiplications
      over ciphertext, but it has a limit of depth
      in the circuit evaluated
- Fully Homomorphic Encryption (FHE)
    - Unlimited number of multiplications and additions

This project focus on the most simple variant: PHE. We
focus on that, because it is the one we could use in
real world cases, due to its simplicity and speed.

## The project

This application is an open-source project,
submited as BCS degree (Bachelor Computer
Science) final project at UFSC -
Universidade Federal de Santa Catarina, Brazil by
Anthony Bernardo Kamers, in 2023. There is a MIT license,
so you can use as you wish.

The code is a very simple Flask application to serve
the server and the client. The database is a
SQLite database. The user interface is made with
Jinja2 templates. Also, the user can choose between
the PHE schemes: Paillier, Damgard-Jurik
and Okamoto-Uchiyama. With that alternatives,
we can check the difference of speed towards each
of them, and check the amazing result without the
backend knowing what the user is querying.

The **Okamoto-Uchiyama** scheme was implemented as part
of this job as well. The references used are in each
Python file, demonstrating what was used as basis.
