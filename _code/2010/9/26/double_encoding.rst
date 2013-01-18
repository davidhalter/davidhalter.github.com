public: yes
tags: [mysql]
summary: Double encoding problems with mysql

Double Encoding / Full Text Problems with MySQL 5.1
===================================================

.. warning ::

    This is an old blog post. I don't recommend to use mysql at all.  Switch to
    `PostgreSQL <http://www.postgresql.org/>`_, as I did, it's so much better.

As I updated MySQL from 5.0 to 5.1 (due to Debian I'm not always as uptodate as
others) I realized that I had huge problems with the fulltext indexes.

The following FTS example seemed not to work:

.. sourcecode:: sql

    CREATE TABLE IF NOT EXISTS `fullTextTable` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(80) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    PRIMARY KEY (`id`),
    FULLTEXT KEY `nameFull` (`name`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8;

    insert into `fullTextTable` (name) values('bärtsch'),('börtsch'),('böll'),('büll');

    select * from `fullTextTable` where match(name) against('+bärtsch' in boolean mode);

    drop table `fullTextTable`;
    -----------------------------
    Returns:
    +----+----------+
    | id | name |
    +----+----------+
    | 1 | bärtsch |
    | 2 | börtsch |
    | 3 | böll |
    +----+----------+

With the help of the MySQL forums I realized that the cause was a double
encoding. The length of ``böll`` for example was not 5, but 7.

Solving it was not a huge thing, just one query:

.. sourcecode:: sql

    update test set fileNew = binary convert(file using latin1)

Since the MySQL convert command doesn't work the expected way, you have to use
the binary command before the convert.

To check if everything worked out the way i wanted it, I used:

.. sourcecode:: sql

    select * from test where file != convert(convert((binary fileNew) using latin1) using utf8);

The double encoding was just a little bug in my php interface: I did not use
"set names utf8". Setting it after connecting has solved my problems.

If you plan on using fulltext indexes, I would seriously recommend checking
your charsets.
