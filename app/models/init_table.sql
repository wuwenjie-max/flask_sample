create database if not exists test default character set utf8mb4 collate utf8mb4_0900_ai_ci;
use test;

create table if not exists user (
    `id`        INT             NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    `name`      VARCHAR(20)     NOT NULL COMMENT '用户名',
    `password`  VARCHAR(20)     NOT NULL COMMENT '',
    `phone`     VARCHAR(20)     DEFAULT '' COMMENT '手机号',
    `created_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    unique index (name)
) engine = InnoDB;

insert into user (name, password, phone) values ('admin', 'admin', '10086');