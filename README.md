<div align="center">

  # 4주차 - sns_backend

</div>
<br><br>

## 목차
- [개발 기간](#--개발-기간--)  
- [프로젝트 설명 및 분석](#-프로젝트)
- [기술 스택](#기술-스택) 
<br><br>

<h2> ⌛ 개발 기간  </h2> 
 2022/07/20  ~ 
 <br><br>
  </div> 


# 💻 프로젝트
  ### 프로젝트 설명
  - 사용자는 본 서비스에 접속하여, 게시물을 업로드 하거나 다른 사람의 게시물을 확인하고, 좋아요를 누를 수 있습니다.
      - JTW 토큰 발급 - 사용자 인증으로 사용
      - 게시글 생성
        - 제목, 내용, 해시태그 필수 입력사항, 해당 API 를 요청한 인증정보에서 추출하여 등록
        - API 단에서 토큰에서 얻은 사용자 정보를 게시글 생성때 작성자로 넣어 사용
- 해시태그는 #로 시작
        - ex) { “hashtags”: “#맛집,#서울,#브런치 카페,#주말”, …} 
          <br>
          <br>



### ERD

- user: 회원 정보
- post: 게시글 정보



<img src="https://user-images.githubusercontent.com/44389424/179910451-9d9fc2e9-bda3-4ce7-ba2e-616f5a5b5133.JPG"/>

<br>
<br>



  ### API 명세서

| ID   | URI                  | METHOD | 기능             |
| ---- | -------------------- | ------ | ---------------- |
| 1    | /api/users/register  | POST   | 회원 가입        |
| 2    | /api/users/login     | POST   | 로그인           |
| 3    | /api/posts           | GET    | 게시글 목록 조회 |
| 4    | /api/posts/<int: id> | GET    | 게시글 상세 조회 |
| 5    | /api/posts           | POST   | 게시글 생성      |
| 6    | /api/posts           | PATCH  | 게시글 수정      |
| 7    | /api/posts           | DELETE | 게시글 삭제      |

<br>
<br>

## API

API 사용법을 안내합니다.



### 회원가입 

회원가입을 합니다. 이메일, 패스워드, 유저네임을 `POST`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
POST /api/users/register HTTP/1.1
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
  "message": "success"
}
```

##### Response:실패

```json
{
  "message": "failed"
}
```



### 로그인 

로그인을 합니다. email, password, access_token을  `POST`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
POST /api/users/login HTTP/1.1
Host: 127.0.0.1:8000
```

##### Header

| Name          | Type   | Description                                          | Required |
| ------------- | ------ | ---------------------------------------------------- | -------- |
| Authorization | String | 액세스 토큰<br/>Bearer ${ACCESS_TOKEN} 형식으로 전달 | O        |



##### Parameter

| Name     | Type     | Description | Required |
| :------- | :------- | :---------- | :------- |
| email    | `String` | 이메일      | O        |
| password | `String` | 패스워드    | O        |



#### Response

| Name   | Type     | Description      |
| :----- | :------- | :--------------- |
| result | `String` | 등록 결과 메세지 |



#### Result

##### Response:성공

```json
{
  "message": "success"
}
```

##### Response:실패

```json
{
    "message": "failed",
    "error": "로그인이 필요합니다."
}
```



### 게시글 목록 조회

게시글 목록을 조회합니다. 다. email, password, access_token을  `GET`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



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
  "message": "success",
  "posts": [
      {
          "id": 1,
          "title": "성수동 맛집 리스트",
          "user_name": "test",
          "create_date": "2022-07-20 18:00:00",
          "좋아요": 10,
          "조회수": 100
      },
      {
          "id": 2,
          "title": "망원동 카페 리스트",
          "user_name": "test2",
          "create_date": "2022-07-21 12:00:00",
          "좋아요": 5,
          "조회수": 30
      },
  ]
}
```

##### Response:실패

```json
{
    "message": "failed",
}
```



### 게시글 상세 조회

게시글 목록을 조회합니다. 다. email, password, access_token을  `GET`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



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
  "message": "success",
  "post": [
      {
          "id": 1,
          "title": "성수동 맛집 리스트",
          "user_name": "test",
          "content": "성수동에 가면 꼭 가봐야할 브런치 맛집 10군데...",
          "hash_tag":  "#맛집,#서울,#브런치 카페,#주말",
          "create_date": "2022-07-20 18:00:00",
          "좋아요": 10,
          "조회수": 100
      },
}
```

##### Response:실패

```json
{
    "message": "failed"
}
```



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
  "message": "success"
}
```

##### Response:실패

```json
{
    "message": "failed",
}
```



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
  "message": "success"
}
```

##### Response:실패

```json
{
    "message": "failed",
}
```



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
  "message": "success"
}
```

##### Response:실패

```json
{
    "message": "failed",
}
```
