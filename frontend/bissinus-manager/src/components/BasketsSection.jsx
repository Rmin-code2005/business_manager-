import { useState, useEffect, useCallback } from 'react'
import BasketDetail from './BasketDetail'
import styles from './BasketsSection.module.css'
import {
  getCryptoBaskets, getCurrencyBaskets, getGoldBaskets,
  getCryptoBasketDetail, getCurrencyBasketDetail, getGoldBasketDetail,
} from '../api/auth'

const BASKET_TYPES = [
  {
    key: 'currency',
    label: 'Currency Baskets',
    icon: '💵',
    color: 'blue',
    listFn: getCurrencyBaskets,
    detailFn: getCurrencyBasketDetail,
  },
  {
    key: 'gold',
    label: 'Gold Baskets',
    icon: '🥇',
    color: 'yellow',
    listFn: getGoldBaskets,
    detailFn: getGoldBasketDetail,
  },
  {
    key: 'crypto',
    label: 'Crypto Baskets',
    icon: '₿',
    color: 'green',
    listFn: getCryptoBaskets,
    detailFn: getCryptoBasketDetail,
  },
]

export default function BasketsSection() {
  // selected = { symbol, type, color, detailFn } | null
  const [selected, setSelected] = useState(null)

  return (
    <div className={styles.section}>
      <div className={styles.sectionHeader}>
        <h2 className={styles.sectionTitle}>My Baskets</h2>
      </div>

      <div className={styles.grid}>
        {BASKET_TYPES.map(t => (
          <BasketList
            key={t.key}
            {...t}
            onSelect={(symbol) => setSelected({
              symbol,
              type: t.key,
              color: t.color,
              detailFn: t.detailFn,
            })}
          />
        ))}
      </div>

      {selected && (
        <BasketDetail
          symbol={selected.symbol}
          type={selected.type}
          color={selected.color}
          fetchFn={selected.detailFn}
          onClose={() => setSelected(null)}
        />
      )}
    </div>
  )
}

// ─── Single basket type list ──────────────────────────────────────────────────
function BasketList({ label, icon, color, listFn, onSelect }) {
  const [items, setItems]     = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState(null)

  useEffect(() => {
    listFn()
      .then(data => {
        // API returns an array of { name: 'USD' }
        setItems(Array.isArray(data) ? data : [])
      })
      .catch(err => setError(err.message || 'Failed to load'))
      .finally(() => setLoading(false))
  }, [listFn])

  return (
    <div className={`${styles.card} ${styles[`card_${color}`]}`}>
      <div className={styles.cardHeader}>
        <span className={styles.cardIcon}>{icon}</span>
        <span className={styles.cardTitle}>{label}</span>
        <span className={styles.cardCount}>
          {items ? items.length : '—'}
        </span>
      </div>

      <div className={styles.cardBody}>
        {loading ? (
          <div className={styles.skeletons}>
            {[1,2,3].map(i => <div key={i} className={styles.skeletonChip} />)}
          </div>
        ) : error ? (
          <div className={styles.empty}>⚠️ {error}</div>
        ) : items.length === 0 ? (
          <div className={styles.empty}>No baskets yet</div>
        ) : (
          <div className={styles.chips}>
            {items.map(item => (
              <button
                key={item.name}
                className={`${styles.chip} ${styles[`chip_${color}`]}`}
                onClick={() => onSelect(item.name)}
              >
                {item.name}
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <path d="M9 18l6-6-6-6"/>
                </svg>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
