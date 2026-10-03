import { Card, CardAction, CardContent, CardHeader } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export function MovieCardSkeleton() {
  return (
    <Card className="w-full max-w-sm" aria-hidden="true">
      <Skeleton className="-mt-(--card-spacing) aspect-2/3 w-full rounded-none" />

      <CardHeader>
        <Skeleton className="h-6 w-3/4" />
        <CardAction>
          <Skeleton className="h-5 w-12 rounded-full" />
        </CardAction>
      </CardHeader>

      <CardContent className="flex flex-col gap-2">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-2/3" />
      </CardContent>
    </Card>
  );
}