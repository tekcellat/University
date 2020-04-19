CREATE DATABASE rk2 OWNER qanelph;

CREATE TABLE cooperator
(
    cooperator_id integer NOT NULL,
    cooperator_department integer,
    cooperator_post text NOT NULL,
    cooperator_name text NOT NULL,
    cooperator_salary float4 NOT NULL,
    PRIMARY KEY (cooperator_id)
);


CREATE TABLE department
(
    department_id integer NOT NULL,
    department_name text NOT NULL,
    department_phone integer NOT NULL,
    department_manager integer,
    PRIMARY KEY (department_id)
);

ALTER TABLE cooperator ADD FOREIGN KEY (cooperator_department) REFERENCES department (department_id);
ALTER TABLE department ADD FOREIGN KEY (department_manager) REFERENCES cooperator (cooperator_id);

DROP TABLE department CASCADE;
DROP TABLE cooperator CASCADE;

INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (1, 1, 'Governor', 'Robena McSparran', 2412);
INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (2, 1, 'Secretary', 'Ardath Olyfant', 12512);
INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (3, 2, 'TechSpecialist', 'Berrie Cobelli', 1235);
INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (4, 2, 'Nurse', 'Jami Bartot', 4255);
INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (5, 3, 'Cleaner', 'Ashien Dallow', 9112);
INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (6, 3, 'Nurse', 'Valene Figures', 500);
INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (7, 4, 'Nurse', 'Wain Sallarie', 100);
INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (8, 4, 'Scientist', 'Kennedy Maddocks', 92000);
INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (9, 5, 'Scientist', 'Elijah Frensch', 1040000);
INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (10, 6, 'Scientist', 'Slava Romanov', 1000000000);
INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (11, 6, 'Nurse', 'Gard Skate', 1242.2);
INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (12, 7, 'Doctor', 'Marjorie Breffit', 22);
INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (13, 8, 'Chemist', 'Alexandre Cyster', 9928);
INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (14, 8, 'Nurse', 'Jamaal Yarrow', 211);
INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (15, 9, 'Guard', 'Neel Quadling', 902);
INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (16, 10, 'Seller', 'Wiley Cheers', 100);
INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (17, 10, 'Seller', 'Bondy Friese', 1299);
INSERT INTO cooperator (cooperator_id, cooperator_department, cooperator_post, cooperator_name, cooperator_salary)
VALUES (18, 11, 'Cooker', 'Arlee Yakovl', 9982.3);

INSERT INTO department (department_id, department_name, department_phone, department_manager)
VALUES (1, 'Governors', 1255135233, 1);
INSERT INTO department (department_id, department_name, department_phone, department_manager)
VALUES (2, 'Secretarys', 1255135243, 4);
INSERT INTO department (department_id, department_name, department_phone, department_manager)
VALUES (3, 'TechSpecialists', 1255135200, 6);
INSERT INTO department (department_id, department_name, department_phone, department_manager)
VALUES (4, 'Nurses', 115133000, 7);
INSERT INTO department (department_id, department_name, department_phone, department_manager)
VALUES (5, 'Scientists', 12532, 9);
INSERT INTO department (department_id, department_name, department_phone, department_manager)
VALUES (6, 'Doctors', 64323, 11);
INSERT INTO department (department_id, department_name, department_phone, department_manager)
VALUES (7, 'Chemists', 42231, 12);
INSERT INTO department (department_id, department_name, department_phone, department_manager)
VALUES (8, 'Guards', 36420, 14);
INSERT INTO department (department_id, department_name, department_phone, department_manager)
VALUES (9, 'Sellers', 23532, 15);
INSERT INTO department (department_id, department_name, department_phone, department_manager)
VALUES (10, 'Cookers', 643234, 16);


CREATE TABLE drug
(
    drug_id integer NOT NULL REFERENCES cooperator (cooperator_id),
    drug_name text NOT NULL,
    drug_instruction text NOT NULL,
    drug_cost float4 NOT NULL,
    PRIMARY KEY (drug_id)
);

INSERT INTO  drug (drug_id,  drug_name,  drug_instruction,  drug_cost)
VALUES (1, 'Furaciclin', 'Stir in water', 150);
INSERT INTO  drug (drug_id,  drug_name,  drug_instruction,  drug_cost)
VALUES (2, 'Ingalipt', 'Spray it', 340);
INSERT INTO  drug (drug_id,  drug_name,  drug_instruction,  drug_cost)
VALUES (3, 'Activirovanniy Ugol', 'Take it inside', 400);
INSERT INTO  drug (drug_id,  drug_name,  drug_instruction,  drug_cost)
VALUES (4, 'Aldumin', 'Take it inside', 1000);
INSERT INTO  drug (drug_id,  drug_name,  drug_instruction,  drug_cost)
VALUES (5, 'Antimorin', 'Stir in water', 1244);
INSERT INTO  drug (drug_id,  drug_name,  drug_instruction,  drug_cost)
VALUES (6, 'Workener', 'Spray it', 1022);
INSERT INTO  drug (drug_id,  drug_name,  drug_instruction,  drug_cost)
VALUES (7, 'HeavySide', 'Take it inside', 400);
INSERT INTO  drug (drug_id,  drug_name,  drug_instruction,  drug_cost)
VALUES (8, 'Treater', 'Stir in water', 500);
INSERT INTO  drug (drug_id,  drug_name,  drug_instruction,  drug_cost)
VALUES (9, 'Magic Spray', 'Spray it', 10);
INSERT INTO  drug (drug_id,  drug_name,  drug_instruction,  drug_cost)
VALUES (10, 'Kiiloosdar', 'Take it inside', 9950);

create table WM (
    id int not null primary key,
    cooperator_id int,
    medicament_id int
);

insert into WM (id, cooperator_id, medicament_id) VALUES (1, 3, 3);
insert into WM (id, cooperator_id, medicament_id) VALUES (2, 1, 5);
insert into WM (id, cooperator_id, medicament_id) VALUES (3, 5, 2);
insert into WM (id, cooperator_id, medicament_id) VALUES (4, 4, 7);
insert into WM (id, cooperator_id, medicament_id) VALUES (5, 2, 10);
insert into WM (id, cooperator_id, medicament_id) VALUES (6, 3, 8);
insert into WM (id, cooperator_id, medicament_id) VALUES (7, 1, 4);
insert into WM (id, cooperator_id, medicament_id) VALUES (8, 8, 1);
insert into WM (id, cooperator_id, medicament_id) VALUES (9, 8, 9);
insert into WM (id, cooperator_id, medicament_id) VALUES (10, 6, 8);