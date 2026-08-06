import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { formatMoney, formatPercent } from "@/lib/formatters";
import type { AllocationItem } from "@/types/dashboard";

interface AllocationBreakdownProps {
  items: AllocationItem[];
  masked?: boolean;
}

/** Render a donut chart segment arc path */
function DonutSegment({
  startAngle,
  endAngle,
  radius,
  strokeWidth,
  colorVar,
}: {
  startAngle: number;
  endAngle: number;
  radius: number;
  strokeWidth: number;
  colorVar: string;
}) {
  const cx = 80;
  const cy = 80;
  const r = radius;
  const saRad = ((startAngle - 90) * Math.PI) / 180;
  const eaRad = ((endAngle - 90) * Math.PI) / 180;

  const x1 = cx + r * Math.cos(saRad);
  const y1 = cy + r * Math.sin(saRad);
  const x2 = cx + r * Math.cos(eaRad);
  const y2 = cy + r * Math.sin(eaRad);

  const large = endAngle - startAngle > 180 ? 1 : 0;

  return (
    <path
      d={`M${x1},${y1} A${r},${r} 0 ${large} 1 ${x2},${y2}`}
      fill="none"
      stroke={`var(${colorVar})`}
      strokeWidth={strokeWidth}
      strokeLinecap="round"
    />
  );
}

export function AllocationBreakdown({ items, masked = false }: AllocationBreakdownProps) {
  const total = items.reduce((sum, i) => sum + i.value, 0);
  const strokeWidth = 28;
  const radius = 60;
  let cumulative = 0;

  const segments = items.map((item) => {
    const proportion = total > 0 ? item.value / total : 0;
    const startAngle = cumulative * 360;
    const endAngle = (cumulative + proportion) * 360;
    cumulative += proportion;
    return { ...item, startAngle, endAngle, proportion };
  });

  if (items.length === 0) {
    return (
      <EmptyState
        title="Dağılım verisi bulunmuyor"
        description="Portföyünüze varlık eklediğinizde dağılım burada görüntülenecektir."
      />
    );
  }

  return (
    <Card>
      <h3 className="text-[16px] leading-[24px] font-semibold text-[var(--color-text-primary)] mb-4">
        Dağılım
      </h3>

      {/* Donut */}
      <div className="flex justify-center" aria-hidden="true">
        <svg viewBox="0 0 160 160" className="w-40 h-40">
          {segments.map((seg, i) => (
            <DonutSegment
              key={i}
              startAngle={seg.startAngle}
              endAngle={seg.endAngle}
              radius={radius}
              strokeWidth={strokeWidth}
              colorVar={seg.colorVar}
            />
          ))}
          <text
            x="80"
            y="74"
            textAnchor="middle"
            className="text-[22px]"
            fontWeight="650"
            fill="var(--color-text-primary)"
          >
            {items.length}
          </text>
          <text
            x="80"
            y="94"
            textAnchor="middle"
            className="text-[11px]"
            fontWeight="500"
            fill="var(--color-text-tertiary)"
          >
            kategori
          </text>
        </svg>
      </div>

      {/* Accessible label list */}
      <ul className="mt-5 space-y-2.5" aria-label="Varlık dağılımı">
        {segments.map((item) => (
          <li
            key={item.category}
            className="flex items-center gap-3 text-sm"
          >
            <span
              className="inline-block h-3 w-3 shrink-0 rounded-full"
              style={{ backgroundColor: `var(${item.colorVar})` }}
              aria-hidden="true"
            />
            <span className="flex-1 text-[var(--color-text-primary)]">
              {item.category}
            </span>
            <span className="tabular-nums text-[var(--color-text-secondary)]">
              {masked ? "₺••••••" : formatMoney(item.value)}
            </span>
            <span className="tabular-nums text-xs text-[var(--color-text-tertiary)] w-12 text-right">
              {formatPercent(item.percentage, true)}
            </span>
          </li>
        ))}
      </ul>

      <div className="sr-only">
        {masked
          ? "Varlık dağılımı gizlilik modunda maskelenmiştir."
          : `Toplam portföy değeri: ${formatMoney(total)}. ${items.map((i) => `${i.category}: ${formatPercent(i.percentage, true)}`).join(", ")}.`}
      </div>
    </Card>
  );
}
