<div align="center">

  # 4주차 - sns_backend

</div>
<br><br>

## 목차
- [개발 기간](#--개발-기간--)  
- [프로젝트 설명 및 분석](#-프로젝트)
- [API 사용법](#API) 
<br><br>

<h2> ⌛ 개발 기간  </h2> 
 2022/07/20  ~ 2022/07/27
 <br><br>
  </div> 


# 💻 프로젝트
  ### 프로젝트 설명 및 분석
  - 사용자는 본 서비스에 접속하여, 게시물을 업로드 하거나 다른 사람의 게시물을 확인하고, 좋아요를 누를 수 있습니다.
      - DRF를 통한 RESTful API 서버 개발
      - JTW 토큰 발급 - 사용자 인증과 게시글 등록, 수정, 삭제, 복원 요청에 사용
          - Permission을 이용하여 권한 부여  
      - Soft Delete 사용 
        - 게시글을 삭제 요청 시 DB에서 바로 삭제하지 않고 임시로 삭제된 상태로 변경

<br>
<br>

### 아키텍처 다이어그램

<img src="https://user-images.githubusercontent.com/44389424/181764366-63f7db23-c4c0-4e95-bce1-80ffef3e1293.jpg"/>

<br>
<br>

### ERD

- tb_user: 회원 정보
- tb_post: 게시글
- tb_post_hashtag: 게시글 해시태그
- tb_post_like: 게시글 좋아요



<img src="https://user-images.githubusercontent.com/44389424/181764359-a2f1b839-2965-403a-90f7-2cc7a807c693.png"/>

<br>
<br>



  ### API 명세서

| METHOD | URI                     | 기능                         |
| ------ | ----------------------- | ---------------------------- |
| POST   | /api/register/          | 회원 가입                    |
| POST   | /api/login/             | 로그인                       |
| POST   | /api/token/refresh/     | 토큰 재발급                  |
| DELETE | /api/users/             | 회원 탈퇴                    |
| GET    | /api/posts/             | 게시글 목록 조회             |
| GET    | /api/posts/<int: id>/   | 게시글 상세 조회             |
| POST   | /api/posts/             | 게시글 생성                  |
| PATCH  | /api/posts/             | 게시글 수정                  |
| DELETE | /api/posts/             | 게시글 삭제                  |
| POST   | /api/<int: id>/like     | 좋아요                       |
| GET    | /api/restore/           | soft delete 게시글 목록 조회 |
| PATCH  | /api/restore/<int: id>/ | soft delete 게시글 복원      |

<br>
<br>

## API

API 사용법을 안내합니다.



### 회원가입 

회원가입을 합니다. 이메일, 패스워드, 유저네임을 `POST`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
POST /api/register/ HTTP/1.1
Host: 127.0.0.1:8000
```

##### Parameter

| Name            | Type       | Description | Required |
|:----------------| :--------- |:------------| :------- |
| email           | `String`   | 이메일         | O        |
| user_name       | `String`   | 유저 네임       | O        |
| password        | `String`      | 패스워드        | O        |




#### Response

| Name   | Type     | Description      |
| :----- | :------- | :--------------- |
| result | `String` | 등록 결과 메세지 |



#### Result

##### Response:성공

```json
{
  "message": "회원가입이 완료되었습니다."
}
```

##### Response:실패

```json
{
  "message": "failed"
}
```

<br>

### 로그인 

로그인을 합니다. email, password, access_token을  `POST`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
POST /api/login/ HTTP/1.1
Host: 127.0.0.1:8000
```



##### Parameter

| Name     | Type     | Description | Required |
| :------- | :------- | :---------- | :------- |
| email    | `String` | 이메일      | O        |
| password | `String` | 패스워드    | O        |



#### Response

| Name          | Type     | Description      |
| :------------ | :------- | :--------------- |
| result        | `String` | 등록 결과 메세지 |
| access_token  | `String` | access token     |
| refresh_token | `String` | refresh token    |

#### Result

##### Response:성공

```json
{
    "message": "Login 성공",
    "token": {
        "access_token": "access_token",
        "refresh_token": "refresh_token"
    }
}
```

##### Response:실패

```json
{
    "message": "email 또는 password를 확인해주세요."
}
```

<br>

### 토큰 재발급 

refresh_token으로 access_token을 재발급 합니다. refresh_token을  `POST`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
POST /api/token/refresh/ HTTP/1.1
Host: 127.0.0.1:8000
```



##### Parameter

| Name    | Type     | Description   | Required |
| :------ | :------- | :------------ | :------- |
| refresh | `String` | refresh token | O        |



#### Response

| Name         | Type     | Description  |
| :----------- | :------- | :----------- |
| access_token | `String` | access token |



#### Result

##### Response:성공

```json
{
    "access_token": "access_token"
}
```

##### Response:실패

```json
{
    "refresh": "이 필드는 필수 항목입니다."
}
```

<br>

### 회원 탈퇴

회원 탈퇴를 합니다. email을  `POST`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
GET /api/users/ HTTP/1.1
Host: 127.0.0.1:8000
```

##### Header

| Name          | Type   | Description                                          | Required |
| ------------- | ------ | ---------------------------------------------------- | -------- |
| Authorization | String | 액세스 토큰<br/>Bearer ${ACCESS_TOKEN} 형식으로 전달 | O        |



#### Response

| Name   | Type     | Description      |
| :----- | :------- | :--------------- |
| result | `String` | 등록 결과 메세지 |



#### Result

##### Response:성공

```json
{
    "message": "회원 탈퇴가 완료되었습니다."
}
```

##### Response:실패

```json
{
    "message": "해당하는 유저가 없습니다."
}
```

<br>

### 게시글 목록 조회

게시글 목록을 조회합니다. 로그인 상태에서 access_token을  `GET`으로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
GET /api/posts/ HTTP/1.1
Host: 127.0.0.1:8000
```

##### Header

| Name          | Type   | Description                                          | Required |
| ------------- | ------ | ---------------------------------------------------- | -------- |
| Authorization | String | 액세스 토큰<br/>Bearer ${ACCESS_TOKEN} 형식으로 전달 | O        |



#### Response

| Name   | Type     | Description      |
| :----- | :------- | :--------------- |
| result | `String` | 등록 결과 메세지 |



#### Result

##### Response:성공

```json
{
    "게시글 목록": [
        {
            "게시글 번호": 1,
            "제목": "성수동 맛집 리스트",
            "작성자": "test",
            "해시태그": ["#소바", "#에비카츠"],
            "좋아요": 10,
            "조회수": 100,
            "작성일": "2022-07-20 18:00:00",
      }
    ]
}
```

##### Response:실패

```json
{
    "message": "게시글 목록을 가져올 수 없습니다."
}
```

<br>

### 게시글 상세 조회

게시글 목록을 조회합니다. 다. 로그인 상태에서 access_token과 게시글 id를 이용해 `GET`으로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
GET /api/posts/<int:id>/ HTTP/1.1
Host: 127.0.0.1:8000
```

##### Header

| Name          | Type   | Description                                          | Required |
| ------------- | ------ | ---------------------------------------------------- | -------- |
| Authorization | String | 액세스 토큰<br/>Bearer ${ACCESS_TOKEN} 형식으로 전달 | O        |



##### Parameter: Path

| Name | Type  | Description | Required |
| :--- | :---- | :---------- | :------- |
| id   | `int` | 게시글 번호 | O        |



#### Response

| Name   | Type     | Description      |
| :----- | :------- | :--------------- |
| result | `String` | 등록 결과 메세지 |



#### Result

##### Response:성공

```json
{
  "message": "{post_id}번 게시글을 불러왔습니다.",
  "post": [
      {
          "게시글 번호": 1,
          "제목": "성수동 맛집 리스트",
          "작성자": "test",
          "본문": "성수동에서 에비카츠로 제일 맛있는 식당",
          "해시태그": ["#소바", "#에비카츠"],
          "좋아요": 10,
          "조회수": 100,      
          "작성일": "2022-07-20 18:00:00",
          "수정일": "2022-07-20 19:00:00",
          "삭제 유무": "False",
      }
}
```

##### Response:실패

```json
{
    "message": "{post_id}번 게시글이 없습니다."
}
```

<br>

### 게시글 생성

게시글을 생성합니다. 제목, 내용, 해시태그를  `POST`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
POST /api/posts/ HTTP/1.1
Host: 127.0.0.1:8000
```

##### Header

| Name          | Type   | Description                                          | Required |
| ------------- | ------ | ---------------------------------------------------- | -------- |
| Authorization | String | 액세스 토큰<br/>Bearer ${ACCESS_TOKEN} 형식으로 전달 | O        |



##### Parameter

| Name     | Type     | Description | Required |
| :------- | :------- | :---------- | :------- |
| title    | `String` | 제목        | O        |
| content  | `String` | 내용        | O        |
| hash_tag | `String` | 해시태크    | O        |



#### Response

| Name   | Type     | Description      |
| :----- | :------- | :--------------- |
| result | `String` | 등록 결과 메세지 |



#### Result

##### Response:성공

```json
{
    "message": "게시글을 등록했습니다."
}
```

##### Response:실패

```json
{
    "message": "게시글 등록을 실패했습니다.",
}
```

<br>

### 게시글 수정

게시글을 수정합니다. 제목, 내용, 해시태그를  `PATCH`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
PATCH /api/posts/ HTTP/1.1
Host: 127.0.0.1:8000
```

##### Header

| Name          | Type   | Description                                          | Required |
| ------------- | ------ | ---------------------------------------------------- | -------- |
| Authorization | String | 액세스 토큰<br/>Bearer ${ACCESS_TOKEN} 형식으로 전달 | O        |



##### Parameter: Path

| Name | Type  | Description | Required |
| :--- | :---- | :---------- | :------- |
| id   | `int` | 게시글 번호 | O        |

##### Parameter

| Name     | Type       | Description | Required |
| :------- | :--------- | :---------- | :------- |
| title    | ``String`` | 제목        | X        |
| content  | `String`   | 내용        | X        |
| hash_tag | `String`   | 해시태크    | X        |

#### Response

| Name   | Type     | Description      |
| :----- | :------- | :--------------- |
| result | `String` | 등록 결과 메세지 |



#### Result

##### Response:성공

```json
{
  "message": "게시글을 수정했습니다."
}
```

##### Response:실패

```json
{
    "message": "게시글 수정을 실패했습니다.",
}
```

<br>

### 게시글 삭제

게시글을 삭제합니다. 게시글 번호를  `DELETE`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
DELETE /api/posts/ HTTP/1.1
Host: 127.0.0.1:8000
```

##### Header

| Name          | Type   | Description                                          | Required |
| ------------- | ------ | ---------------------------------------------------- | -------- |
| Authorization | String | 액세스 토큰<br/>Bearer ${ACCESS_TOKEN} 형식으로 전달 | O        |

##### Parameter: Path

| Name | Type  | Description | Required |
| :--- | :---- | :---------- | :------- |
| id   | `int` | 게시글 번호 | O        |



#### Response

| Name   | Type     | Description      |
| :----- | :------- | :--------------- |
| result | `String` | 등록 결과 메세지 |



#### Result

##### Response:성공

```json
{
  "message": "{post_id}번 게시글을 삭제했습니다."
}
```

##### Response:실패

```json
{
    "message": "{post_id}번 게시글을 삭제할 수 없습니다.",
}
```

<br>

### 게시글 좋아요

게시글의 좋아요 기능입니다. 게시글 번호,  sel을  `POST`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
DELETE /api/posts/<int:id>/like HTTP/1.1
Host: 127.0.0.1:8000
```

##### Header

| Name          | Type   | Description                                          | Required |
| ------------- | ------ | ---------------------------------------------------- | -------- |
| Authorization | String | 액세스 토큰<br/>Bearer ${ACCESS_TOKEN} 형식으로 전달 | O        |

##### Parameter: Path

| Name | Type  | Description | Required |
| :--- | :---- | :---------- | :------- |
| id   | `int` | 게시글 번호 | O        |

##### Parameter

| Name | Type       | Description                        | Required |
| :--- | :--------- | :--------------------------------- | :------- |
| sel  | ``String`` | like: 좋아요, dislike: 좋아요 취소 | O        |



#### Response

| Name   | Type     | Description      |
| :----- | :------- | :--------------- |
| result | `String` | 등록 결과 메세지 |



#### Result

##### Response:성공

```json
{
  "message": "{post_id}번 게시글의 좋아요를 눌렸습니다."
}
```

##### Response:실패

```json
{
    "message": "{post_id}번 게시글의 좋아요를 눌렸습니다."
}
```

<br>

### Soft Delete 게시글 목록 조회

Soft Delete 게시글 목록을 조회합니다. 로그인 상태에서 access_token을  `GET`으로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
GET /api/resotre/ HTTP/1.1
Host: 127.0.0.1:8000
```

##### Header

| Name          | Type   | Description                                          | Required |
| ------------- | ------ | ---------------------------------------------------- | -------- |
| Authorization | String | 액세스 토큰<br/>Bearer ${ACCESS_TOKEN} 형식으로 전달 | O        |



#### Response

| Name   | Type     | Description      |
| :----- | :------- | :--------------- |
| result | `String` | 등록 결과 메세지 |



#### Result

##### Response:성공

```json
{
    "message": "{user_name}의 휴지통에 있는 게시글 목록을 가져왔습니다.",
    "data": [
        {
           "게시글 번호": 1,
           "제목": "성수동 맛집 리스트",
           "작성자": "test",
           "본문": "성수동에서 에비카츠로 제일 맛있는 식당",
           "해시태그": ["#소바", "#에비카츠"],
           "좋아요": 10,
           "조회수": 100,      
           "작성일": "2022-07-20 18:00:00",
           "수정일": "2022-07-20 19:00:00",
           "삭제 유무": "True",
      }
    ]
}
```

##### Response:실패

```json
{
    "message": "{user_name}의 휴지통에 있는 게시글 목록을 가져오지 못했습니다."
}
```

<br>

### Soft Delete 게시글 복원

Soft Delete 게시글을 복원합니다. 로그인 상태에서 access_token과 게시글 번호를  `PATCH`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
PATCH /api/resotre/<int:id> HTTP/1.1
Host: 127.0.0.1:8000
```

##### Header

| Name          | Type   | Description                                          | Required |
| ------------- | ------ | ---------------------------------------------------- | -------- |
| Authorization | String | 액세스 토큰<br/>Bearer ${ACCESS_TOKEN} 형식으로 전달 | O        |



#### Response

| Name   | Type     | Description      |
| :----- | :------- | :--------------- |
| result | `String` | 등록 결과 메세지 |



#### Result

##### Response:성공

```json
{
    "message": "{post_id}번 게시글을 복원했습니다.",
    "data": [
        {
           "게시글 번호": 1,
           "제목": "성수동 맛집 리스트",
           "작성자": "test",
           "본문": "성수동에서 에비카츠로 제일 맛있는 식당",
           "해시태그": ["#소바", "#에비카츠"],
           "좋아요": 10,
           "조회수": 100,      
           "작성일": "2022-07-20 18:00:00",
           "수정일": "2022-07-20 19:00:00",
      }
    ]
}
```

##### Response:실패

```json
{
    "message": "{post_id}번 게시글을 복원 할 수 없습니다."
}
```

<br>

