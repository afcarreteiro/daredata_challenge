DO
$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'ds_user_role') THEN
        CREATE ROLE ds_user_role;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'mle_user_role') THEN
        CREATE ROLE mle_user_role;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'ds_user') THEN
        CREATE USER ds_user WITH PASSWORD 'ds_user';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'mle_user') THEN
        CREATE USER mle_user WITH PASSWORD 'mle_user';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE companydata TO ds_user;
GRANT CONNECT ON DATABASE companydata TO mle_user;

GRANT ds_user_role TO ds_user;
GRANT mle_user_role TO mle_user;

ALTER SCHEMA public OWNER TO admin;
GRANT USAGE ON SCHEMA public TO ds_user_role;
GRANT USAGE, CREATE ON SCHEMA public TO mle_user_role;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO ds_user_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mle_user_role;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ds_user_role;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mle_user_role;

ALTER DEFAULT PRIVILEGES FOR USER admin IN SCHEMA public
GRANT SELECT ON TABLES TO ds_user_role;

ALTER DEFAULT PRIVILEGES FOR USER admin IN SCHEMA public
GRANT ALL PRIVILEGES ON TABLES TO mle_user_role;

ALTER DEFAULT PRIVILEGES FOR USER admin IN SCHEMA public
GRANT USAGE, SELECT ON SEQUENCES TO ds_user_role;

ALTER DEFAULT PRIVILEGES FOR USER admin IN SCHEMA public
GRANT ALL PRIVILEGES ON SEQUENCES TO mle_user_role;
