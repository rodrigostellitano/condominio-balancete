PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE monthly_balance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT NOT NULL UNIQUE,              
        previous_balance REAL NOT NULL,
        paid_quotas INTEGER NOT NULL CHECK(paid_quotas >= 0),
        paid_with_fine INTEGER NOT NULL CHECK(paid_with_fine >= 0),
        tags INTEGER NOT NULL CHECK(tags >= 0)
    , total_income REAL DEFAULT 0, total_expense REAL DEFAULT 0, current_balance REAL DEFAULT 0);
INSERT INTO monthly_balance VALUES(2,'01-2026',11500.500000000000166,2,4,3,3348.0,2530.9200000000000585,12317.579999999999085);
INSERT INTO monthly_balance VALUES(3,'02-2026',11500.500000000000166,2,4,3,3348.0,2530.9200000000000585,12317.579999999999085);
CREATE TABLE income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT NOT NULL,
        description TEXT NOT NULL,
        amount REAL NOT NULL CHECK(amount >= 0),
        FOREIGN KEY (month) REFERENCES monthly_balance(month)
            ON DELETE CASCADE
    );
INSERT INTO income VALUES(7,'01-2026','Total Cotas',2800.0);
INSERT INTO income VALUES(8,'01-2026','Qtd Cotas Pagas',28.0);
INSERT INTO income VALUES(9,'01-2026','Qtd Cotas Pagas Multa',4.0);
INSERT INTO income VALUES(10,'01-2026','Qtd Tag',3.0);
INSERT INTO income VALUES(11,'01-2026','Total Cotas com Multa',488.0);
INSERT INTO income VALUES(12,'01-2026','Total Tag',60.0);
INSERT INTO income VALUES(13,'02-2026','Total Cotas',2800.0);
INSERT INTO income VALUES(14,'02-2026','Qtd Cotas Pagas',28.0);
INSERT INTO income VALUES(15,'02-2026','Qtd Cotas Pagas Multa',4.0);
INSERT INTO income VALUES(16,'02-2026','Qtd Tag',3.0);
INSERT INTO income VALUES(17,'02-2026','Total Cotas com Multa',488.0);
INSERT INTO income VALUES(18,'02-2026','Total Tag',60.0);
CREATE TABLE expense (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT NOT NULL,
        description TEXT NOT NULL,
        amount REAL NOT NULL CHECK(amount >= 0),
        FOREIGN KEY (month) REFERENCES monthly_balance(month)
            ON DELETE CASCADE
    );
INSERT INTO expense VALUES(6,'01-2026','Sindico + Limpeza',1680.0);
INSERT INTO expense VALUES(7,'01-2026','Light (01/2026)',111.5299999999999958);
INSERT INTO expense VALUES(8,'01-2026','FNT',99.989999999999987778);
INSERT INTO expense VALUES(9,'01-2026','Conserto de Telefone e Camera',240.0);
INSERT INTO expense VALUES(10,'01-2026','Saco de Lixo',399.39999999999997726);
INSERT INTO expense VALUES(11,'02-2026','Sindico + Limpeza',1680.0);
INSERT INTO expense VALUES(12,'02-2026','Light (01/2026)',111.5299999999999958);
INSERT INTO expense VALUES(13,'02-2026','FNT',99.989999999999987778);
INSERT INTO expense VALUES(14,'02-2026','Conserto de Telefone e Camera',240.0);
INSERT INTO expense VALUES(15,'02-2026','Saco de Lixo',399.39999999999997726);
CREATE TABLE arrears (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT NOT NULL,
    house_number INTEGER NOT NULL,
    reference_month INTEGER NOT NULL,
    reference_year INTEGER NOT NULL,

    FOREIGN KEY (month) REFERENCES monthly_balance(month)
        ON DELETE CASCADE,

    UNIQUE(house_number, reference_month, reference_year,month)
);
INSERT INTO arrears VALUES(11,'01-2026',8,1,2025);
INSERT INTO arrears VALUES(12,'01-2026',8,2,2025);
INSERT INTO arrears VALUES(13,'01-2026',8,3,2025);
INSERT INTO arrears VALUES(14,'01-2026',8,4,2025);
INSERT INTO arrears VALUES(15,'01-2026',8,5,2025);
INSERT INTO arrears VALUES(16,'01-2026',8,6,2026);
INSERT INTO arrears VALUES(17,'01-2026',8,7,2026);
INSERT INTO arrears VALUES(18,'01-2026',18,1,2025);
INSERT INTO arrears VALUES(19,'01-2026',18,2,2025);
INSERT INTO arrears VALUES(20,'01-2026',18,3,2026);
INSERT INTO arrears VALUES(21,'02-2026',8,1,2025);
INSERT INTO arrears VALUES(22,'02-2026',8,2,2025);
INSERT INTO arrears VALUES(23,'02-2026',8,3,2025);
INSERT INTO arrears VALUES(24,'02-2026',8,4,2025);
INSERT INTO arrears VALUES(25,'02-2026',8,5,2025);
INSERT INTO arrears VALUES(26,'02-2026',8,6,2026);
INSERT INTO arrears VALUES(27,'02-2026',8,7,2026);
INSERT INTO arrears VALUES(28,'02-2026',18,1,2025);
INSERT INTO arrears VALUES(29,'02-2026',18,2,2025);
INSERT INTO arrears VALUES(30,'02-2026',18,3,2026);
CREATE TABLE management (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT NOT NULL,
    role TEXT NOT NULL,
    name TEXT NOT NULL,

    FOREIGN KEY (month) REFERENCES monthly_balance(month)
        ON DELETE CASCADE
);
INSERT INTO management VALUES(5,'01-2026','Sindico','Rodrigo Stellitano Pereira');
INSERT INTO management VALUES(6,'01-2026','Presidente','Nielza');
INSERT INTO management VALUES(7,'01-2026','Fiscal','Carlos Francisco');
INSERT INTO management VALUES(8,'01-2026','Fiscal','Rose');
INSERT INTO management VALUES(9,'02-2026','Sindico','Rodrigo Stellitano Pereira');
INSERT INTO management VALUES(10,'02-2026','Presidente','Nielza');
INSERT INTO management VALUES(11,'02-2026','Fiscal','Carlos Francisco');
INSERT INTO management VALUES(12,'02-2026','Fiscal','Rose');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('monthly_balance',3);
INSERT INTO sqlite_sequence VALUES('income',18);
INSERT INTO sqlite_sequence VALUES('expense',15);
INSERT INTO sqlite_sequence VALUES('arrears',30);
INSERT INTO sqlite_sequence VALUES('management',12);
COMMIT;
