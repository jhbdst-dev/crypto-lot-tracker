# package.json

## 역할

프로젝트 전체 설정 파일

## 구성

- name
- version
- scripts
- dependencies
- devDependencies

## 기억할 것

npm run dev

↓

package.json

↓

scripts

↓

vite 실행

### package.json

역할

- 프로젝트의 설정 파일
- 프로젝트 정보 저장
- 실행 명령어(scripts) 관리
- 필요한 라이브러리 관리

핵심

npm run dev를 실행하면 package.json의 scripts에서 dev를 찾아 Vite를 실행한다.
