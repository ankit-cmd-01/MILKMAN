import { Link } from "react-router-dom";

const plans = [
  {
    title: "Daily Plan",
    description: "Receive fresh milk and essentials every day.",
    frequency: "DAILY",
  },
  {
    title: "Weekly Plan",
    description: "Scheduled deliveries every week at your convenience.",
    frequency: "WEEKLY",
  },
];

function SubscriptionPlansPage() {
  return (
    <main className="mx-auto max-w-6xl px-4 py-10 md:px-6">
      <h1 className="font-serif text-4xl font-bold text-black">Subscription Plans</h1>
      <p className="mt-2 text-[#333333]">Choose between daily and weekly subscription frequencies.</p>

      <div className="mt-8 grid gap-6 md:grid-cols-2">
        {plans.map((plan) => (
          <section key={plan.frequency} className="card-surface p-6">
            <h2 className="font-serif text-2xl font-semibold text-black">{plan.title}</h2>
            <p className="mt-2 text-sm text-[#333333]">{plan.description}</p>
            <ul className="mt-4 list-inside list-disc space-y-1 text-sm text-[#333333]">
              <li>Dynamic price calculation in backend</li>
              <li>Pause, resume and cancel supported</li>
              <li>Track status and payment history</li>
            </ul>
            <Link to="/products" className="btn-primary mt-5 inline-block rounded-xl px-4 py-2 text-sm">
              Subscribe Now
            </Link>
          </section>
        ))}
      </div>
    </main>
  );
}

export default SubscriptionPlansPage;
