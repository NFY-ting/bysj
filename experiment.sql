/*
Navicat MySQL Data Transfer

Source Server         : yun
Source Server Version : 50505
Source Host           : chentingting
Source Database       : experiment

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2021-05-19 20:49:51
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for classes
-- ----------------------------
DROP TABLE IF EXISTS `classes`;
CREATE TABLE `classes` (
  `class_id` int(8) unsigned NOT NULL,
  `class_name` varchar(50) NOT NULL,
  `class_code` varchar(15) NOT NULL,
  `tec_id` int(10) unsigned NOT NULL,
  `total` int(3) unsigned DEFAULT NULL,
  PRIMARY KEY (`class_id`),
  KEY `tec_id` (`tec_id`),
  CONSTRAINT `classes_ibfk_1` FOREIGN KEY (`tec_id`) REFERENCES `teachers` (`tec_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of classes
-- ----------------------------
INSERT INTO `classes` VALUES ('20161105', '计科2016级嵌入式', '05qr', '202102', '16');
INSERT INTO `classes` VALUES ('20171103', '计科2017级网络工程', '03jk', '202101', '6');
INSERT INTO `classes` VALUES ('20171104', '计科2017级软件工程', '74rg', '202101', '6');
INSERT INTO `classes` VALUES ('20181104', '计科2018级软件工程', '04rg', '202103', '18');

-- ----------------------------
-- Table structure for classgrade
-- ----------------------------
DROP TABLE IF EXISTS `classgrade`;
CREATE TABLE `classgrade` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `class_id` int(8) unsigned NOT NULL,
  `lab_id` int(5) unsigned NOT NULL,
  `tec_id` int(10) unsigned NOT NULL,
  `num` int(5) unsigned NOT NULL DEFAULT 0 COMMENT '完成人数',
  `rate` double(5,2) unsigned NOT NULL DEFAULT 0.00 COMMENT '实验完成率',
  PRIMARY KEY (`id`),
  KEY `class_id_2033` (`class_id`),
  KEY ` lab_id_234` (`lab_id`),
  KEY `tec_id_323` (`tec_id`),
  CONSTRAINT ` lab_id_234` FOREIGN KEY (`lab_id`) REFERENCES `labs` (`lab_id`) ON DELETE NO ACTION,
  CONSTRAINT `class_id_2033` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`) ON DELETE NO ACTION,
  CONSTRAINT `tec_id_323` FOREIGN KEY (`tec_id`) REFERENCES `teachers` (`tec_id`) ON DELETE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of classgrade
-- ----------------------------
INSERT INTO `classgrade` VALUES ('1', '20171103', '1', '202101', '6', '1.00');
INSERT INTO `classgrade` VALUES ('2', '20171103', '2', '202101', '2', '0.33');
INSERT INTO `classgrade` VALUES ('3', '20171103', '3', '202101', '5', '0.83');
INSERT INTO `classgrade` VALUES ('4', '20171103', '4', '202101', '4', '0.67');
INSERT INTO `classgrade` VALUES ('5', '20171103', '5', '202101', '3', '0.50');
INSERT INTO `classgrade` VALUES ('6', '20171104', '2', '202101', '4', '0.68');
INSERT INTO `classgrade` VALUES ('7', '20171104', '5', '202101', '3', '0.50');

-- ----------------------------
-- Table structure for grades
-- ----------------------------
DROP TABLE IF EXISTS `grades`;
CREATE TABLE `grades` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `stu_id` int(10) unsigned NOT NULL,
  `class_id` int(8) unsigned NOT NULL,
  `lab_id` int(5) unsigned NOT NULL,
  `grade` enum('0','1') DEFAULT '0',
  `tec_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `stu_id` (`stu_id`),
  KEY `class_id` (`class_id`),
  KEY `lab_id` (`lab_id`),
  KEY `grades_ibfk_4` (`tec_id`),
  CONSTRAINT `grades_ibfk_1` FOREIGN KEY (`stu_id`) REFERENCES `students` (`stu_id`),
  CONSTRAINT `grades_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`),
  CONSTRAINT `grades_ibfk_3` FOREIGN KEY (`lab_id`) REFERENCES `labs` (`lab_id`),
  CONSTRAINT `grades_ibfk_4` FOREIGN KEY (`tec_id`) REFERENCES `teachers` (`tec_id`)
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of grades
-- ----------------------------
INSERT INTO `grades` VALUES ('49', '2017110302', '20171103', '1', '1', '202101');
INSERT INTO `grades` VALUES ('50', '2017110303', '20171103', '1', '1', '202101');
INSERT INTO `grades` VALUES ('51', '2017110304', '20171103', '1', '1', '202101');
INSERT INTO `grades` VALUES ('52', '2017110305', '20171103', '1', '1', '202101');
INSERT INTO `grades` VALUES ('53', '2017110306', '20171103', '1', '1', '202101');
INSERT INTO `grades` VALUES ('54', '2017110352', '20171103', '1', '1', '202101');
INSERT INTO `grades` VALUES ('67', '2017110302', '20171103', '3', '1', '202101');
INSERT INTO `grades` VALUES ('68', '2017110303', '20171103', '3', '1', '202101');
INSERT INTO `grades` VALUES ('69', '2017110304', '20171103', '3', '1', '202101');
INSERT INTO `grades` VALUES ('70', '2017110305', '20171103', '3', '1', '202101');
INSERT INTO `grades` VALUES ('71', '2017110306', '20171103', '3', '0', '202101');
INSERT INTO `grades` VALUES ('72', '2017110352', '20171103', '3', '1', '202101');
INSERT INTO `grades` VALUES ('79', '2017110302', '20171103', '4', '1', '202101');
INSERT INTO `grades` VALUES ('80', '2017110303', '20171103', '4', '1', '202101');
INSERT INTO `grades` VALUES ('81', '2017110304', '20171103', '4', '1', '202101');
INSERT INTO `grades` VALUES ('82', '2017110305', '20171103', '4', '1', '202101');
INSERT INTO `grades` VALUES ('83', '2017110306', '20171103', '4', '0', '202101');
INSERT INTO `grades` VALUES ('84', '2017110352', '20171103', '4', '0', '202101');
INSERT INTO `grades` VALUES ('85', '2017110307', '20171104', '5', '1', '202101');
INSERT INTO `grades` VALUES ('86', '2017110308', '20171104', '5', '0', '202101');
INSERT INTO `grades` VALUES ('87', '2017110309', '20171104', '5', '1', '202101');
INSERT INTO `grades` VALUES ('88', '2017110310', '20171104', '5', '0', '202101');
INSERT INTO `grades` VALUES ('89', '2017110311', '20171104', '5', '1', '202101');
INSERT INTO `grades` VALUES ('90', '2017110401', '20171104', '5', '0', '202101');
INSERT INTO `grades` VALUES ('91', '2017110307', '20171104', '2', '1', '202101');
INSERT INTO `grades` VALUES ('92', '2017110308', '20171104', '2', '0', '202101');
INSERT INTO `grades` VALUES ('93', '2017110309', '20171104', '2', '1', '202101');
INSERT INTO `grades` VALUES ('94', '2017110310', '20171104', '2', '1', '202101');
INSERT INTO `grades` VALUES ('95', '2017110311', '20171104', '2', '1', '202101');
INSERT INTO `grades` VALUES ('96', '2017110401', '20171104', '2', '0', '202101');
INSERT INTO `grades` VALUES ('97', '2017110302', '20171103', '2', '0', '202101');
INSERT INTO `grades` VALUES ('98', '2017110303', '20171103', '2', '0', '202101');
INSERT INTO `grades` VALUES ('99', '2017110304', '20171103', '2', '1', '202101');
INSERT INTO `grades` VALUES ('100', '2017110305', '20171103', '2', '0', '202101');
INSERT INTO `grades` VALUES ('101', '2017110306', '20171103', '2', '1', '202101');
INSERT INTO `grades` VALUES ('102', '2017110352', '20171103', '2', '0', '202101');
INSERT INTO `grades` VALUES ('103', '2017110302', '20171103', '5', '0', '202101');
INSERT INTO `grades` VALUES ('104', '2017110303', '20171103', '5', '0', '202101');
INSERT INTO `grades` VALUES ('105', '2017110304', '20171103', '5', '1', '202101');
INSERT INTO `grades` VALUES ('106', '2017110305', '20171103', '5', '0', '202101');
INSERT INTO `grades` VALUES ('107', '2017110306', '20171103', '5', '1', '202101');
INSERT INTO `grades` VALUES ('108', '2017110352', '20171103', '5', '1', '202101');

-- ----------------------------
-- Table structure for labs
-- ----------------------------
DROP TABLE IF EXISTS `labs`;
CREATE TABLE `labs` (
  `lab_id` int(5) unsigned NOT NULL AUTO_INCREMENT,
  `lab_name` varchar(30) NOT NULL,
  `lab_info` varchar(200) DEFAULT NULL,
  `lab_aim` varchar(100) DEFAULT NULL,
  `flag` varchar(50) DEFAULT NULL,
  `lab_url` varchar(100) NOT NULL COMMENT '实验地址链接',
  `lab_img` varchar(100) DEFAULT NULL COMMENT '实验封面图片',
  PRIMARY KEY (`lab_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of labs
-- ----------------------------
INSERT INTO `labs` VALUES ('1', 'XSS之基础实验', '本实验为一个注册表单，包括多个输入框，是XSS攻击发生最常见的场景', '初步认识XSS攻击方式和危害；应寻求多种xss攻击方式，从而达到举一反三的目的', 'XSsCroSS--', 'https://www.baidu.com/', '../uploads/xss1.jpg');
INSERT INTO `labs` VALUES ('2', 'XSS之进阶实验', '通过观察payload寻找漏洞切入点；解析关键词绕过', '想呢我还不和我爸的荷包蛋回家恶补的金额我不会的 ', 'ThjVOmXP*', 'https://www.baidu.com/', '../uploads/xss2.jpg');
INSERT INTO `labs` VALUES ('3', 'SQL注入之字符型', '通过输入单引号是否会导致错误；输入双引号有无异常（因为’’是单引号的转义形式）说明此处极有可能存在输入为字符串类型的SQL注入', '认识字符型SQL注入；初步掌握SQL注入流程；了解SQL注入防御', 'jbsxhjsb', 'https://www.baidu.com/', '../uploads/sql1.jpg');
INSERT INTO `labs` VALUES ('4', 'SQL注入之数字型', '以MYSQL为例子说明，SQL注入的形成原理是没有对用户输入的数据进行过滤和转义，使得用户的数据被SQL解释器执行。数字型的注入特征是当输入的参数为整型时，如：ID，年龄，页码等，若存在注入漏洞，则可认为是数字型注入。数字型的注入多存在ASP与PHP等弱类型中。', '1.了解SQL注入的基本原理  2.掌握PHP脚本访问MySQL数据库的基本方法  3.掌握程序设计中避免出现SQL注入漏洞的基本方法', 'jbsxhjsb', 'https://www.baidu.com/', '../uploads/sql2.jpg');
INSERT INTO `labs` VALUES ('5', '任意文件上传', '文件上传漏洞是指用户上传了一个可执行的脚本文件，并通过此脚本文件获得了执行服务器端命令的能力。常见场景是web服务器允许用户上传图片或者普通文本文件保存，而用户绕过上传机制上传恶意代码并执行从而控制服', '认识文件上传检测包括客户端javascript检测、服务端Content-Type类型检测、服务端path参数检测、服务端文件扩展名检测、服务端内容检测', 'xjnwecdwej', 'https://www.baidu.com/', '../uploads/OIP.jpg');

-- ----------------------------
-- Table structure for students
-- ----------------------------
DROP TABLE IF EXISTS `students`;
CREATE TABLE `students` (
  `stu_id` int(10) unsigned NOT NULL COMMENT '学号',
  `stu_name` varchar(50) NOT NULL COMMENT '学生姓名',
  `pwd` varchar(100) DEFAULT 'student01' COMMENT '密码',
  `sex` enum('male','female') DEFAULT 'male' COMMENT '性别',
  `email` varchar(50) DEFAULT NULL COMMENT '邮箱',
  `class_id` int(20) unsigned DEFAULT NULL COMMENT '班级id',
  PRIMARY KEY (`stu_id`),
  KEY `class_idcdc` (`class_id`),
  CONSTRAINT `class_idcdc` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of students
-- ----------------------------
INSERT INTO `students` VALUES ('2017110302', '陈婷婷', 'pbkdf2:sha256:150000$OaCdvw89$8adc03def01c8fb6d158d4f338872d6d38cffa0ff35bd36694108af18f2ca3af', 'female', 'nfy_ting@qq.com', '20171103');
INSERT INTO `students` VALUES ('2017110303', '杜思若', 'pbkdf2:sha256:150000$OVogFSPN$6eb8e0fbae7eb6ddb71173fdd0f52cdf302f55aa23dfea65f0d088e0bdf4c1cd', 'female', 'cxdcce@cdew.com', '20171103');
INSERT INTO `students` VALUES ('2017110304', '康祺祥', 'pbkdf2:sha256:150000$EeYZNQ4u$255c8a386c6f908924cb5e233e1e38b366e26c6324b3e80c7f89ca4ab45a4bba', 'male', 'chbrbmm@cdew.com', '20171103');
INSERT INTO `students` VALUES ('2017110305', '吴会', 'pbkdf2:sha256:150000$hoA1Iq3X$867112af776a42a21b5130a8897fd01f358db6501ec0d0a39b153391668bf58f', 'female', 'iuwenciue@cdew.com', '20171103');
INSERT INTO `students` VALUES ('2017110306', '汤莺韵', 'pbkdf2:sha256:150000$ASwrLxyn$4cbf14adcb59d6d38cae4edc54925b7833c69d938b4113f364a7555f2d0a5974', 'female', 'cwnccnw@cdew.com', '20171103');
INSERT INTO `students` VALUES ('2017110307', '蒋勇军', 'pbkdf2:sha256:150000$WlpufZpF$4219ee8d1e28146f370bd81795835f69703cb30814ab2bf3f15574ad3ee45308', 'male', 'okonbcd@cdew.com', '20171104');
INSERT INTO `students` VALUES ('2017110308', '谢雪', 'pbkdf2:sha256:150000$KHEpyGLt$8961b935393b5a3872a819fbd7a6949bd93d06e3411f228efae0b190b3c33f28', 'female', 'okonbcd@cdew.com', '20171104');
INSERT INTO `students` VALUES ('2017110309', '廖志', 'pbkdf2:sha256:150000$mRTpbIJ3$07641199265d19118102e6361f70971fa48db6272bc7ff06d044d7feedcedcf0', 'male', 'okonbcd@cdew.com', '20171104');
INSERT INTO `students` VALUES ('2017110310', '董飞', 'pbkdf2:sha256:150000$VSWesURd$c8cb514968cfcf9d18b343dd758325a86e7c92175a37be95856355c8288ca2b2', 'male', 'okonbcd@cdew.com', '20171104');
INSERT INTO `students` VALUES ('2017110311', '杨雅美', 'pbkdf2:sha256:150000$HaZmLbkK$ec2647158309c917318164a5071ccf539dafab948c069af1dd104a189da24e31', 'female', 'okonbcd@cdew.com', '20171104');
INSERT INTO `students` VALUES ('2017110352', '张振', 'pbkdf2:sha256:150000$vb0uoJHv$28e636c47e23e3c4d6c3bfc03ee1a25c8f51f864a1a0d4c00d31ae792baf1065', 'male', 'wyefdtye@cec.xcd', '20171103');
INSERT INTO `students` VALUES ('2017110401', '阿布事', 'pbkdf2:sha256:150000$0GktFoa1$c7d69d20683a8f3d1650fa9b0ede9837cabd3199532c954b31a3e4788235e62c', 'male', 'jndcjds@cec.xcd', '20171104');

-- ----------------------------
-- Table structure for teachers
-- ----------------------------
DROP TABLE IF EXISTS `teachers`;
CREATE TABLE `teachers` (
  `tec_id` int(10) unsigned NOT NULL COMMENT '职工号',
  `tec_name` varchar(50) NOT NULL COMMENT '教师名',
  `pwd` varchar(100) DEFAULT '1101teacher',
  `sex` enum('male','female') DEFAULT 'male',
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`tec_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of teachers
-- ----------------------------
INSERT INTO `teachers` VALUES ('123456', 'admin', 'guanliyuan', 'male', null);
INSERT INTO `teachers` VALUES ('202101', '张宇', '1101teacher', 'male', 'pkzhang@qq.com');
INSERT INTO `teachers` VALUES ('202102', '项亦为', '1101teacher', 'male', 'xjnwejcn@qq.com');
INSERT INTO `teachers` VALUES ('202103', '王鸢', '1101teacher', 'female', 'ncieuwcn@qq.com');
