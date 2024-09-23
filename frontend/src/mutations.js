import gql from 'graphql-tag';

export const USER_SIGNUP = gql`
  mutation (
    $username: String!
    $email: String!
    $password: String!
  ) {
    createUser(
      username: $username
      email: $email
      password: $password
    ) {
      user {
        id
        username
      }
    }
  }`;

  export const USER_SIGNIN = gql`
    mutation (
      $username: String!
      $password: String!
    ) {
      tokenAuth(
        username: $username
        password: $password
      ) {
        token
        user {
          id
          username
        }
      }
    }`;