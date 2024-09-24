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

    export const ADD_EXERCISE = gql`
      mutation (
        $name: String!
        $description: String!
        $block: Int!
        $order_in_block: Int!
        $sets: Int!
        $reps: Int!
        $program: String!
      ) {
        createExercise(
          name: $name
          description: $description
          block: $block
          orderInBlock: $order_in_block
          sets: $sets
          reps: $reps
          program: $program
        ) {
          exercise {
            id
            name
            description
            block
            orderInBlock
            sets
            reps
            program {
              id
              name
            }
          }
        }
      }`;
      