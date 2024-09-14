import { createClient } from "@/utils/supabase/server";
import { InfoIcon } from "lucide-react"; // Check if it's used
import { redirect } from "next/navigation";
import { NotesPanel } from '@/components/notes-panel';

export default async function ProtectedPage() {
  const supabase = createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return redirect("/sign-in");
  }

  return (
    <NotesPanel />
  ); // <-- Added this closing parenthesis for the return
} // <-- Added this closing curly brace for the function
