import Foundation
import Capacitor
import StoreKit

/// The one in-app purchase: "Full Game", a non-consumable that unlocks everything past the free exhibition game.
/// StoreKit 2, so the App Store signs every transaction and the device verifies it; nothing goes to a server of ours.
/// JavaScript calls it as plugin "Store" (see the native layer in the game's src/native.js):
///   product   -> the localized price to show on the unlock screen
///   purchase  -> buy it (result: purchased / cancelled / pending)
///   restore   -> App Store sync, then whether it is owned (the Restore Purchases button)
///   owned     -> whether this Apple ID owns it (checked at launch and whenever the app comes back)
@objc(StorePlugin)
public class StorePlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "StorePlugin"
    public let jsName = "Store"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "product", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "purchase", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "restore", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "owned", returnType: CAPPluginReturnPromise),
    ]

    private var updates: Task<Void, Never>?

    /// Transactions that finish outside a purchase call (Ask to Buy approved later, a purchase interrupted by the
    /// app closing, a refund) arrive here; finishing them is required. The game re-checks ownership on resume.
    override public func load() {
        updates = Task.detached {
            for await result in Transaction.updates {
                if case .verified(let transaction) = result { await transaction.finish() }
            }
        }
    }

    deinit { updates?.cancel() }

    private static func isOwned(_ productId: String) async -> Bool {
        for await result in Transaction.currentEntitlements {
            if case .verified(let transaction) = result, transaction.productID == productId, transaction.revocationDate == nil {
                return true
            }
        }
        return false
    }

    @objc func product(_ call: CAPPluginCall) {
        guard let productId = call.getString("productId") else { call.reject("productId is required"); return }
        Task {
            do {
                guard let product = try await Product.products(for: [productId]).first else { call.reject("product_not_found"); return }
                call.resolve(["id": product.id, "displayPrice": product.displayPrice, "title": product.displayName])
            } catch {
                call.reject(error.localizedDescription)
            }
        }
    }

    @objc func purchase(_ call: CAPPluginCall) {
        guard let productId = call.getString("productId") else { call.reject("productId is required"); return }
        Task {
            do {
                guard let product = try await Product.products(for: [productId]).first else { call.reject("product_not_found"); return }
                let result = try await product.purchase()
                switch result {
                case .success(let verification):
                    switch verification {
                    case .verified(let transaction):
                        await transaction.finish()
                        call.resolve(["result": "purchased", "owned": true])
                    case .unverified(_, _):
                        call.resolve(["result": "unverified", "owned": false])
                    }
                case .userCancelled:
                    call.resolve(["result": "cancelled", "owned": false])
                case .pending:
                    call.resolve(["result": "pending", "owned": false])
                @unknown default:
                    call.resolve(["result": "unknown", "owned": false])
                }
            } catch {
                call.reject(error.localizedDescription)
            }
        }
    }

    @objc func restore(_ call: CAPPluginCall) {
        guard let productId = call.getString("productId") else { call.reject("productId is required"); return }
        Task {
            var synced = true
            do { try await AppStore.sync() } catch { synced = false }   // the player can cancel the sign-in sheet
            let owned = await StorePlugin.isOwned(productId)
            call.resolve(["owned": owned, "synced": synced])
        }
    }

    @objc func owned(_ call: CAPPluginCall) {
        guard let productId = call.getString("productId") else { call.reject("productId is required"); return }
        Task {
            let owned = await StorePlugin.isOwned(productId)
            call.resolve(["owned": owned])
        }
    }
}
