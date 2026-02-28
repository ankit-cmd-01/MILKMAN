import { useToast } from "../context/ToastContext";

const toastTheme = {
  success: "border-l-4 border-lightBlue bg-white text-black",
  error: "border-l-4 border-black bg-white text-black",
  info: "border-l-4 border-lightBrown bg-white text-black",
};

function ToastContainer() {
  const { toasts } = useToast();

  return (
    <div className="pointer-events-none fixed right-4 top-4 z-[100] flex w-full max-w-sm flex-col gap-2">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={`pointer-events-auto rounded-xl border border-[#EAEAEA] px-4 py-3 text-sm shadow-sm ${toastTheme[toast.type] || toastTheme.info}`}
        >
          {toast.message}
        </div>
      ))}
    </div>
  );
}

export default ToastContainer;
