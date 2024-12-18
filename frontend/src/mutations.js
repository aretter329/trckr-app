import gql from 'graphql-tag';

export const USER_SIGNUP = gql`
  mutation (
    $username: String!
    $email: String!
    $password: String!
    $isAthlete: Boolean!
    $isCoach: Boolean!
    $firstName: String!
    $lastName: String!
  ) {
    createUser(
      username: $username
      email: $email
      password: $password
      isAthlete: $isAthlete
      isCoach: $isCoach
      firstName: $firstName
      lastName: $lastName
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
        isCoach
        isAthlete
        firstName
        lastName
        email
        coach{
          username
        }
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

  export const LOG_WORKOUT = gql`
  mutation (
    $athleteUsername: String!
    $workoutId: ID!
    $sets: [LoggedSetInput]!
    $notes: String!
    $assignedDate: Date!
  ) {
    logWorkout(
      athleteUsername: $athleteUsername
      workoutId: $workoutId
      sets: $sets
      notes: $notes
      assignedDate: $assignedDate
    ) {
      loggedWorkout {
        id
        athlete{
        username
        }
      }
    }
  }`;

  export const CREATE_WORKOUT_GROUP = gql`
  mutation (
    $name: String!
    $coach: String!
  ) {
    createWorkoutGroup(
      name: $name
      coach: $coach
    ) {
      workoutGroup {
        id
        name
        coach{
          username
        }
      }
    }
  }`;

  export const ADD_ATHLETE_TO_GROUP = gql`
  mutation (
    $athleteId: ID!
    $groupId: ID!
  ) {
    addAthleteToGroup(
      athleteId: $athleteId
      groupId: $groupId
    ) {
      group {
        athletes{
          username
        }
      }
    }
  }`;

  export const UPDATE_LOGGED_SETS = gql`
  mutation (
    $loggedWorkoutId: ID!
    $loggedSets: [LoggedSetInput]!
  ) {
    updateLoggedSets(
      loggedWorkoutId: $loggedWorkoutId
      loggedSets: $loggedSets
    ) {
      loggedWorkout {
        id
      }
      
    }
  }`;

  export const ADD_EXERCISE_NAME = gql`
  mutation (
    $name: String!
    $author: String!
  ) {
    addExerciseName(
      name: $name
      author: $author
    ) {
      exercise {
        id
        name
        author{
          username
        }
      }
    }
  }`;

  export const UPDATE_PASSWORD = gql`
  mutation (
    $username: String!
    $newPassword: String!
  ) {
    updatePassword(
      username: $username
      newPassword: $newPassword
    ) {
      user {
        id
        username
      }
    }
  }`;