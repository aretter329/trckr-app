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

    export const ADD_PROGRAM = gql`
      mutation (
        $title: String!
        $notes: String!
        $author: String!
        $tags: [String]!
        $slug: String!
      ) {
        createProgram(
          title: $title
          notes: $notes
          author: $author
          tags: $tags
          slug: $slug
        ) {
          program {
            id
            title
            notes
            author{
              username
            }
            slug
          }
          
        }
        
      }`;
      
    export const ADD_WORKOUT = gql`
      mutation (
        $type: String!
        $orderInDay: Int!
        $dayId: ID!
      ) {
        createWorkout(
          type: $type
          orderInDay: $orderInDay
          dayId: $dayId
        ) {
          workout {
            id
            type
            orderInDay
            day {
              id
            }
          }
        }
      }`;

    export const ADD_DAY = gql`
      mutation (
        $name: String!
        $orderInProgram: Int!
        $programId: ID!
      ) {
        createDay(
          name: $name
          orderInProgram: $orderInProgram
          programId: $programId
        ) {
          day {
            id
            name
            orderInProgram
            program {
              id
            }
          }
        }
      }`;


    export const ADD_EXERCISE = gql`
      mutation (
        $name: String!
        $description: String!
        $block: Int!
        $orderInBlock: Int!
        $workoutId: ID!
      ) {
        createExercise(
          name: $name
          description: $description
          block: $block
          orderInBlock: $orderInBlock
          workoutId: $workoutId
        ) {
          exercise {
            id
            name
            description
            block
            orderInBlock
            workout {
            id
            }
          }
        }
      }`;

    export const ADD_SET = gql`
      mutation (
        $reps: Int!
        $weight: Int!
        $number: Int!
        $exerciseId: ID!
      ) {
        createSet(
          reps: $reps
          weight: $weight
          number: $number
          exerciseId: $exerciseId
        ) {
          set {
            id
            reps
            weight
            number
            exercise {
              id
            }
          }
        }
      }`;
      