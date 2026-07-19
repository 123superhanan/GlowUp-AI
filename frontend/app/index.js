import { Redirect } from "expo-router";

export default function EntryRedirect() {
  // Routes the unauthenticated user directly into the login screen on application boot
  return <Redirect href="/Onboarding" />;
}
