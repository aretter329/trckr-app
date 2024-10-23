import gql from 'graphql-tag';

export const USER_SIGNUP = gql`
  mutation (
    $username: String!
    $email: String!
    $password: String!
    $isAthlete: Boolean!
    $isCoach: Boolean!
  ) {
    createUser(
      username: $username
      email: $email
      password: $password
      isAthlete: $isAthlete
      isCoach: $isCoach
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
        $assignedAthletes: [String]!
        $days: [DayInputType]!
      ) {
        createProgram(
          title: $title
          notes: $notes
          author: $author
          tags: $tags
          slug: $slug
          assignedAthletes: $assignedAthletes
          days: $days
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
        $workoutId: ID!
      ) {
        createExercise(
          name: $name
          description: $description
          block: $block
          workoutId: $workoutId
        ) {
          exercise {
            id
            name
            description
            block
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


    export const ADD_ATHLETE = gql`
      mutation (
        $athleteUsername: String!
        $coachUsername: String!
      ) {
        addAthlete(
          athleteUsername: $athleteUsername
          coachUsername: $coachUsername
        ) {
          user {
            id
            username
          }
        }
      }`;
      

      export const ASSIGN_PROGRAM = gql`
      mutation (
        $programId: ID!
        $athleteUsername: String!
      ) {
        assignProgram(
          programId: $programId
          athleteUsername: $athleteUsername
        ) {
          program {
            id
            title
          }
        }
      }`;